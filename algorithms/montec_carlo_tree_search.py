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
    def __init__(self, game: G, n_rollouts=1000, use_cache=True):
        super().__init__(game)
        self.n_rollouts = n_rollouts
        self.use_cache = use_cache
        self.root = None

    def select(self, node: Node, is_opponent: bool) -> Node:
        if len(node.children) == 0:
            return node, is_opponent
        return self.select(max(node.children, key=self.ucb), not is_opponent)

    def expand(self, node: Node, is_oponnent: bool):
        if self.game.is_terminal_state(node.game_state):
            return node
        node.children = [
            Node(parent=node, game_state=self.game.take_action(node.game_state, a), action=a)
            for a in self.game.actions_for(node.game_state, is_oponnent)
        ]
        return random.choice(node.children)

    def playout(self, current_state: State) -> float:
        is_opponent = True
        while not self.game.is_terminal_state(current_state):
            action = random.choice(self.game.actions_for(current_state, is_opponent))
            current_state = self.game.take_action(current_state, action)
            is_opponent = not is_opponent
        return current_state, self.game.reward(current_state)

    def propagate(self, reward: float, node: Node) -> None:
        node.visits += 1
        node.wins += (reward > 0) * reward
        if node.parent:
            self.propagate(-reward, node.parent)

    def choose_action(self, state: State) -> None:
        self.root = self._find_root(state) 
        for _ in range(self.n_rollouts):
            expanded_node = self.expand(*self.select(self.root, False))
            _, reward = self.playout(expanded_node.game_state)
            self.propagate(reward, expanded_node)
            self.best_action = max(self.root.children, key=lambda n: n.visits).action

    def _find_root(self, state: State) -> Node:
        if self.root is None or not self.cache:  # first call
            return Node(game_state=state) 
        oponnent_node = next((n for n in self.root.children if n.action == self.best_action), None)
        if oponnent_node is None: 
            # __eq__() method was implemented incorrectly in action class, or best_action was not updated during last call
            return Node(game_state=state) 
        current_node = next((n for n in oponnent_node.children if n.game_state == state), None)      
        return current_node or Node(game_state=state) 

    @staticmethod
    def ucb(node: Node, c=1.4) -> float:
        return (
            float("inf")
            if node.visits == 0
            else node.wins / node.visits + c * math.sqrt(math.log(node.parent.visits) / node.visits)
        )
