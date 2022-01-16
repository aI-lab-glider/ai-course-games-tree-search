from __future__ import annotations
from base.bot import Bot, G
from base.state import State
from base.action import Action
import math
from typing import Optional, List
from dataclasses import dataclass, field
import random


@dataclass
class Node:
    wins: int = 0 
    visits: int = 0 
    game_state: State = None
    parent: Node = None
    action: Action = None
    children: List[Node] = field(default_factory=list)


class MCTS(Bot):
    def __init__(self, game: G, n_rollouts=1000):
        super().__init__(game)
        self.n_rollouts = n_rollouts


    def select(self, node: Node, is_opponent: bool) -> Node:
        return (node, is_opponent) if len(node.children) == 0 else self.select(max(node.children, key=self.ucb), not is_opponent)


    def expand(self, node: Node, is_oponnent: bool):
        if self.game.is_terminal_state(node.game_state):
            return node
        node.children = [
            Node(parent=node, game_state=self.game.take_action(node.game_state, a), action=a)
            for a in self.game.actions_for(node.game_state, is_oponnent) 
        ]
        return random.choice(node.children)


    def playout(self,  current_state: State) -> float:
        is_opponent = True
        while not self.game.is_terminal_state(current_state):
            action = random.choice(self.game.actions_for(current_state, is_opponent))
            current_state = self.game.take_action(current_state, action)
            is_opponent = not is_opponent
        return current_state, self.game.reward(current_state)

    
    def propagate(self, reward: float, node: Node) -> None:
        node.visits += 1 
        if reward > 0:
            node.wins += reward 
        if node.parent:
            self.propagate(-reward, node.parent)

    
    def choose_action(self, state: State) -> Optional[Action]:
        root = Node(game_state=state)
        for _ in range(self.n_rollouts):
            expanded_node = self.expand(*self.select(root, False))
            _, reward = self.playout(expanded_node.game_state)
            self.propagate(reward, expanded_node)
        return max(root.children, key=lambda n: n.visits).action

    
    @staticmethod
    def ucb(node: Node, c=1.4) -> float:
        return float('inf') if node.visits == 0 else node.wins / node.visits + c * math.sqrt(math.log(node.parent.visits) / node.visits)
