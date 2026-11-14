import random
import unittest

from last_tile.contracts import GameState
from last_tile.game import apply_move, is_terminal, legal_moves, new_game
from last_tile.ai.alphabeta import alphabeta_search
from last_tile.ai.minimax import minimax_search


def random_state(rng: random.Random, plies: int) -> GameState:
    """Random non-terminal state reached after `plies` moves from the start."""
    while True:
        s = new_game()
        for _ in range(plies):
            if is_terminal(s):
                break
            s = apply_move(s, rng.choice(legal_moves(s)))
        if not is_terminal(s):
            return s


class TestAlphaBeta(unittest.TestCase):
    def test_returns_legal_move(self):
        s = new_game()
        r = alphabeta_search(s, depth=3)
        self.assertIn(r.move, legal_moves(s))
        self.assertGreater(r.stats.nodes_visited, 1)
        self.assertEqual(r.stats.completed_depth, 3)

    def test_invalid_depth_raises(self):
        with self.assertRaises(ValueError):
            alphabeta_search(new_game(), depth=0)

    def test_terminal_root_returns_none(self):
        # Player 0 at (0,0) fully boxed in by blocked tiles / opponent.
        s = GameState(positions=((0, 0), (1, 1)),
                      blocked=frozenset({(0, 1), (1, 0)}), to_move=0)
        self.assertTrue(is_terminal(s))
        r = alphabeta_search(s, depth=2)
        self.assertIsNone(r.move)
        self.assertEqual(r.score, -10_000.0)

    def test_takes_win_in_one_ply(self):
        # P0 at (0,0) can move to (0,1) which traps P1 at (0,2).
        s = GameState(size=3,
                      positions=((0, 0), (0, 2)),
                      blocked=frozenset({(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}),
                      to_move=0)
        # P0 legal: (0,1), (1,0). Moving to (0,1) leaves P1 with no moves.
        r = alphabeta_search(s, depth=2)
        self.assertEqual(r.move, (0, 1))
        self.assertEqual(r.score, 10_000.0)

    def test_equivalent_to_minimax(self):
        rng = random.Random(2024)
        checked = 0
        for plies in range(0, 13):
            for _ in range(4):
                s = random_state(rng, plies)
                for depth in (1, 2, 3):
                    ab = alphabeta_search(s, depth)
                    mm = minimax_search(s, depth)
                    self.assertEqual(ab.move, mm.move, (s, depth))
                    self.assertEqual(ab.score, mm.score, (s, depth))
                    self.assertLessEqual(ab.stats.nodes_visited, mm.stats.nodes_visited)
                    checked += 1
        self.assertGreater(checked, 100)

    def test_prunes_at_depth_3_and_4(self):
        s = new_game()
        for depth in (3, 4):
            ab = alphabeta_search(s, depth)
            mm = minimax_search(s, depth)
            self.assertGreater(ab.stats.cutoff_events, 0)
            self.assertLess(ab.stats.nodes_visited, mm.stats.nodes_visited)
            self.assertEqual((ab.move, ab.score), (mm.move, mm.score))

    def test_no_cutoffs_at_depth_1(self):
        self.assertEqual(alphabeta_search(new_game(), 1).stats.cutoff_events, 0)


if __name__ == "__main__":
    unittest.main()
