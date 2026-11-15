"""Unit tests for Member A (board rules, transitions, and heuristic)."""
import unittest

from last_tile.contracts import GameState
from last_tile.game import (
    apply_move,
    evaluate,
    is_terminal,
    legal_moves,
    new_game,
    winner,
)


class TestMemberA(unittest.TestCase):
    def test_new_game_initial_state(self) -> None:
        state = new_game(5)
        self.assertEqual(state.size, 5)
        self.assertEqual(state.positions, ((0, 0), (4, 4)))
        self.assertEqual(state.blocked, frozenset())
        self.assertEqual(state.to_move, 0)
        self.assertFalse(is_terminal(state))
        self.assertIsNone(winner(state))

    def test_corner_knight_moves(self) -> None:
        state = new_game(5)
        self.assertEqual(legal_moves(state, 0), ((1, 2), (2, 1)))
        self.assertEqual(legal_moves(state, 1), ((2, 3), (3, 2)))

    def test_center_knight_moves_and_jumping_over_blocked_tiles(self) -> None:
        adjacent_ring = frozenset(
            {
                (1, 1), (1, 2), (1, 3),
                (2, 1),         (2, 3),
                (3, 1), (3, 2), (3, 3),
            }
        )
        state = GameState(
            size=5,
            positions=((2, 2), (4, 4)),
            blocked=adjacent_ring,
            to_move=0,
        )
        expected = (
            (0, 1), (0, 3),
            (1, 0), (1, 4),
            (3, 0), (3, 4),
            (4, 1), (4, 3),
        )
        self.assertEqual(legal_moves(state, 0), expected)

    def test_blocked_and_occupied_destinations_excluded(self) -> None:
        state = GameState(
            size=5,
            positions=((0, 0), (1, 2)),
            blocked=frozenset(),
            to_move=0,
        )
        self.assertEqual(legal_moves(state, 0), ((2, 1),))

    def test_apply_move_blocks_previous_tile_and_switches_turn(self) -> None:
        s0 = new_game(5)
        s1 = apply_move(s0, (1, 2))

        self.assertEqual(s1.positions, ((1, 2), (4, 4)))
        self.assertEqual(s1.blocked, frozenset({(0, 0)}))
        self.assertEqual(s1.to_move, 1)
        self.assertEqual(s0.positions, ((0, 0), (4, 4)))
        self.assertEqual(s0.blocked, frozenset())

    def test_illegal_moves_rejected(self) -> None:
        state = new_game(5)
        with self.assertRaises(ValueError):
            apply_move(state, (0, 1))
        with self.assertRaises(ValueError):
            apply_move(state, (-1, 2))

        s1 = apply_move(state, (1, 2))
        with self.assertRaises(ValueError):
            apply_move(s1, (0, 0))

    def test_terminal_win_detection(self) -> None:
        trapped_state = GameState(
            size=5,
            positions=((0, 0), (4, 4)),
            blocked=frozenset({(1, 2), (2, 1)}),
            to_move=0,
        )
        self.assertTrue(is_terminal(trapped_state))
        self.assertEqual(winner(trapped_state), 1)

    def test_evaluate_antisymmetry_and_exact_score(self) -> None:
        start = new_game(5)
        self.assertEqual(evaluate(start, 0), 0.0)
        self.assertEqual(evaluate(start, 1), 0.0)

        mid = GameState(
            size=5,
            positions=((2, 2), (4, 4)),
            blocked=frozenset(),
            to_move=0,
        )
        self.assertEqual(evaluate(mid, 0), 64.0)
        self.assertEqual(evaluate(mid, 0), -evaluate(mid, 1))

    def test_invalid_player_rejected(self) -> None:
        state = new_game(5)
        with self.assertRaises(ValueError):
            legal_moves(state, 2)
        with self.assertRaises(ValueError):
            evaluate(state, -1)


if __name__ == "__main__":
    unittest.main()