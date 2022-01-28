from __future__ import annotations
from base.bot import A, Bot, G
from base.state import State
from base.action import Action
import math
from typing import Generic, Optional, List, Tuple
from dataclasses import dataclass, field
import random


@dataclass
class Node(Generic[A]):
    game_state: State
    accumulated_reward: float = 0
    visits: int = 0
    parent: Optional[Node] = None
    action: Optional[A] = None
    children: List[Node[A]] = field(default_factory=list)

    def is_leaf(self):
        return len(self.children) == 0


class MCTS(Bot[G, A]):
    def __init__(self, game: G, n_rollouts=1000, use_cache=True):
        super().__init__(game)
        self.n_rollouts = n_rollouts
        self.use_cache = use_cache
        self.root: Optional[Node[A]] = None

    def choose_action(self, state: State) -> None:
        self.root = self._find_root(state)
        for _ in range(self.n_rollouts):
            expanded_node = self._expand(*self._select(self.root, False))
            reward = self._playout(expanded_node.game_state)
            self._propagate(reward, expanded_node)
            self.best_action = max(self.root.children, key=lambda n: n.visits).action

    def _find_root(self, state: State) -> Node:
        if self.root is None or not self.use_cache:  # first call
            return Node(game_state=state)

        opponent_node = next((n for n in self.root.children if n.action == self.best_action), None)
        if opponent_node is None:
            # __eq__() method was implemented incorrectly in action class, or best_action was not updated during last call
            return Node(game_state=state)
        current_node = next((n for n in opponent_node.children if n.game_state == state), None)
        return current_node or Node(game_state=state)

    def _select(self, node: Node, is_opponent: bool) -> Tuple[Node, bool]:
        if node.is_leaf():
            return node, is_opponent
        predicate = max if not is_opponent else min
        return self._select(predicate(node.children, key=self.ucb), not is_opponent)

    def _expand(self, node: Node, is_oponnent: bool):
        if self.game.is_terminal_state(node.game_state):
            return node
        node.children = [
            Node(parent=node, game_state=self.game.take_action(node.game_state, a), action=a)
            for a in self.game.actions_for(node.game_state, is_oponnent)
        ]
        return random.choice(node.children)

    def _playout(self, current_state: State) -> float:
        is_opponent = True
        while not self.game.is_terminal_state(current_state):
            action = random.choice(self.game.actions_for(current_state, is_opponent))
            current_state = self.game.take_action(current_state, action)
            is_opponent = not is_opponent
        return self.game.reward(current_state)

    def _propagate(self, reward: float, node: Node) -> None:
        node.visits += 1
        node.accumulated_reward += (reward > 0) * reward
        if node.parent:
            self._propagate(-reward, node.parent)

    @staticmethod
    def ucb(node: Node, c=1.4) -> float:
        return (
            float("inf")
            if node.visits == 0 or node.parent is None
            else node.accumulated_reward / node.visits + c * math.sqrt(math.log(node.parent.visits) / node.visits)
        )
