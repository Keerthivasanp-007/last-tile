"""Smoke tests verifying the initial scaffold imports and frozen contracts work."""
import unittest
from last_tile.contracts import GameState, SearchResult, SearchStats
from last_tile import game
from last_tile.ai import alphabeta, hill_climbing, minimax


class TestScaffold(unittest.TestCase):
    def test_contracts_and_new_game(self) -> None:
        state = game.new_game(size=5)
        self.assertIsInstance(state, GameState)
        self.assertEqual(state.size, 5)
        self.assertEqual(state.positions, ((0, 0), (4, 4)))
        self.assertEqual(len(state.blocked), 0)
        self.assertEqual(state.to_move, 0)

        stats = SearchStats(nodes_visited=8, completed_depth=1)
        res = SearchResult(move=(0, 1), score=12.0, stats=stats)
        self.assertEqual(res.move, (0, 1))
        self.assertEqual(res.stats.nodes_visited, 8)

    def test_invalid_board_size_rejected(self) -> None:
        with self.assertRaises(ValueError):
            game.new_game(size=1)

    def test_unimplemented_stubs_raise_not_implemented(self) -> None:
        state = game.new_game(size=5)
        with self.assertRaises(NotImplementedError):
            game.legal_moves(state)
        with self.assertRaises(NotImplementedError):
            game.evaluate(state, root_player=0)
        with self.assertRaises(NotImplementedError):
            hill_climbing.hill_climbing_search(state)
        with self.assertRaises(NotImplementedError):
            minimax.minimax_search(state, depth=3)
        with self.assertRaises(NotImplementedError):
            alphabeta.alphabeta_search(state, depth=3)


if __name__ == "__main__":
    unittest.main()
