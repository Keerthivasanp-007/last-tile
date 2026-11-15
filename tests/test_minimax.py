"""Tests for Algorithm 2: Minimax search (Member B). Knight-move rules."""

import unittest

from last_tile.ai.minimax import minimax_search
from last_tile.contracts import GameState
from last_tile.game import legal_moves, new_game


class TestMinimaxSearch(unittest.TestCase):

    def test_returns_legal_move(self):
        state = new_game()
        result = minimax_search(state, depth=2)
        self.assertIn(result.move, legal_moves(state))

    def test_nodes_visited_greater_than_one(self):
        result = minimax_search(new_game(), depth=2)
        self.assertGreater(result.stats.nodes_visited, 1)

    def test_depth_one_counts(self):
        # Depth 1: the root plus one child per legal move, each child evaluated.
        # From (0, 0) a knight has 2 moves: (1, 2) and (2, 1).
        state = new_game()
        num_moves = len(legal_moves(state))
        self.assertEqual(num_moves, 2)
        result = minimax_search(state, depth=1)
        self.assertEqual(result.stats.nodes_visited, 1 + num_moves)
        self.assertEqual(result.stats.leaf_evaluations, num_moves)

    def test_completed_depth_and_time(self):
        result = minimax_search(new_game(), depth=3)
        self.assertEqual(result.stats.completed_depth, 3)
        self.assertGreaterEqual(result.stats.elapsed_ms, 0.0)

    def test_invalid_depth_raises_value_error(self):
        with self.assertRaises(ValueError):
            minimax_search(new_game(), depth=0)
        with self.assertRaises(ValueError):
            minimax_search(new_game(), depth=-1)

    def test_terminal_root_returns_no_move(self):
        # Player 0 at (0, 0) can only jump to (1, 2) or (2, 1); both are
        # blocked, so the root is already terminal.
        state = GameState(
            size=5,
            positions=((0, 0), (4, 4)),
            blocked=frozenset({(1, 2), (2, 1)}),
            to_move=0,
        )
        result = minimax_search(state, depth=3)
        self.assertIsNone(result.move)
        self.assertEqual(result.score, -10_000.0)
        self.assertEqual(result.stats.nodes_visited, 1)

    def test_chooses_win_in_one_ply(self):
        # Player 1 at (4, 4) can only jump to (2, 3) or (3, 2); (3, 2) is
        # blocked. Player 0 at (0, 2) can jump to (2, 3) and trap Player 1.
        # P0's moves are (1, 0), (1, 4), (2, 1), (2, 3); the winner is last.
        state = GameState(
            size=5,
            positions=((0, 2), (4, 4)),
            blocked=frozenset({(3, 2)}),
            to_move=0,
        )
        for depth in (1, 2, 3):
            result = minimax_search(state, depth=depth)
            self.assertEqual(result.move, (2, 3))
            self.assertEqual(result.score, 10_000.0)

    def test_tie_keeps_first_move_in_sorted_order(self):
        # Player 1's only escape squares are (2, 3) and (3, 2). (3, 2) is
        # blocked and Player 0 stands on (2, 3). Whatever Player 0 does,
        # (2, 3) becomes blocked and Player 1 is trapped, so every move
        # scores 10_000.0. P0's moves: (0, 2), (0, 4), (1, 1), (3, 1), (4, 2).
        # Strict improvement means the first one, (0, 2), must be kept.
        state = GameState(
            size=5,
            positions=((2, 3), (4, 4)),
            blocked=frozenset({(3, 2)}),
            to_move=0,
        )
        self.assertEqual(
            legal_moves(state), ((0, 2), (0, 4), (1, 1), (3, 1), (4, 2))
        )
        for depth in (1, 3):
            result = minimax_search(state, depth=depth)
            self.assertEqual(result.score, 10_000.0)
            self.assertEqual(result.move, (0, 2))

    def test_same_input_gives_same_result(self):
        state = new_game()
        first = minimax_search(state, depth=3)
        second = minimax_search(state, depth=3)
        self.assertEqual(first.move, second.move)
        self.assertEqual(first.score, second.score)


if __name__ == "__main__":
    unittest.main()
