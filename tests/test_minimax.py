"""Tests for Algorithm 2: Minimax search (Member B)."""

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
        state = new_game()
        num_moves = len(legal_moves(state))
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
        # Player 0 at (0, 0) is boxed in, so the root is already terminal.
        state = GameState(
            size=5,
            positions=((0, 0), (4, 4)),
            blocked=frozenset({(0, 1), (1, 0), (1, 1)}),
            to_move=0,
        )
        result = minimax_search(state, depth=3)
        self.assertIsNone(result.move)
        self.assertEqual(result.score, -10_000.0)
        self.assertEqual(result.stats.nodes_visited, 1)

    def test_chooses_win_in_one_ply(self):
        # Player 1 at (4, 4) has only (3, 4) free. Player 0 at (2, 4)
        # can move into (3, 4) and trap Player 1 immediately.
        state = GameState(
            size=5,
            positions=((2, 4), (4, 4)),
            blocked=frozenset({(3, 3), (4, 3)}),
            to_move=0,
        )
        # Depths 1 and 2: only (3, 4) is a guaranteed win within the search.
        for depth in (1, 2):
            result = minimax_search(state, depth=depth)
            self.assertEqual(result.move, (3, 4))
            self.assertEqual(result.score, 10_000.0)

    def test_tie_keeps_first_move_in_sorted_order(self):
        # Same state, depth 3: (1, 3), (1, 4), (2, 3) and (3, 4) all win.
        # They tie at 10_000.0, so the first one in sorted order is kept.
        state = GameState(
            size=5,
            positions=((2, 4), (4, 4)),
            blocked=frozenset({(3, 3), (4, 3)}),
            to_move=0,
        )
        result = minimax_search(state, depth=3)
        self.assertEqual(result.score, 10_000.0)
        self.assertEqual(result.move, (1, 3))

    def test_same_input_gives_same_result(self):
        state = new_game()
        first = minimax_search(state, depth=3)
        second = minimax_search(state, depth=3)
        self.assertEqual(first.move, second.move)
        self.assertEqual(first.score, second.score)


if __name__ == "__main__":
    unittest.main()