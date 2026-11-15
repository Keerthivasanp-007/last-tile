"""Unit tests for Algorithm 1: Steepest-Ascent Hill Climbing (Member D)."""
from __future__ import annotations
import unittest
from last_tile.ai.hill_climbing import hill_climbing_search
from last_tile.contracts import GameState
from last_tile.game import new_game


class TestHillClimbingSearch(unittest.TestCase):
    def test_returns_legal_knight_move_from_start(self) -> None:
        state = new_game(size=5)
        result = hill_climbing_search(state)
        # From (0, 0), legal knight moves on an empty 5x5 board are (1, 2) and (2, 1).
        self.assertIn(result.move, ((1, 2), (2, 1)))
        self.assertEqual(result.stats.completed_depth, 1)

    def test_visits_root_plus_all_immediate_neighbors(self) -> None:
        state = new_game(size=5)
        result = hill_climbing_search(state)
        # Root (1) + 2 legal knight moves from corner (0, 0) = 3 visited states.
        self.assertEqual(result.stats.nodes_visited, 3)
        self.assertEqual(result.stats.leaf_evaluations, 2)
        self.assertEqual(result.stats.cutoff_events, 0)
        self.assertGreaterEqual(result.stats.elapsed_ms, 0.0)

    def test_terminal_root_returns_none_move(self) -> None:
        # Player 0 at (0, 0) has both knight destinations (1, 2) and (2, 1) blocked.
        trapped_state = GameState(
            size=5,
            positions=((0, 0), (4, 4)),
            blocked=frozenset({(1, 2), (2, 1)}),
            to_move=0,
        )
        result = hill_climbing_search(trapped_state)
        self.assertIsNone(result.move)
        self.assertEqual(result.score, -10_000.0)
        self.assertEqual(result.stats.nodes_visited, 1)

    def test_chooses_immediate_winning_trap_move(self) -> None:
        # Player 1 is at (4, 4); its only legal knight moves are (2, 3) and (3, 2).
        # (2, 3) is already blocked, and Player 0 at (1, 1) can jump to (3, 2) to trap Player 1.
        state = GameState(
            size=5,
            positions=((1, 1), (4, 4)),
            blocked=frozenset({(2, 3)}),
            to_move=0,
        )
        result = hill_climbing_search(state)
        self.assertEqual(result.move, (3, 2))
        self.assertEqual(result.score, 10_000.0)

    def test_deterministic_tie_breaking_picks_first_sorted_move(self) -> None:
        # Symmetric start state: (1, 2) and (2, 1) have identical heuristic scores,
        # so strict '>' comparison keeps the first sorted move (1, 2).
        state = new_game(size=5)
        first = hill_climbing_search(state)
        second = hill_climbing_search(state)
        self.assertEqual(first.move, (1, 2))
        self.assertEqual(first.move, second.move)
        self.assertEqual(first.score, second.score)


if __name__ == "__main__":
    unittest.main()