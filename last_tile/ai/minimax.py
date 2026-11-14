"""Algorithm 2: Depth-limited Minimax search for Last Tile (Member B)."""

import math
import time

from last_tile.contracts import GameState, SearchResult, SearchStats
from last_tile.game import apply_move, evaluate, is_terminal, legal_moves, winner

WIN_SCORE = 10_000.0
LOSS_SCORE = -10_000.0


def _minimax_value(
    state: GameState,
    remaining_depth: int,
    root_player: int,
    stats: SearchStats,
) -> float:
    """Return the minimax score of `state`, searching `remaining_depth` more plies."""
    stats.nodes_visited += 1

    # Terminal check comes first.
    if is_terminal(state):
        if winner(state) == root_player:
            return WIN_SCORE
        return LOSS_SCORE

    # Depth cutoff: use the heuristic.
    if remaining_depth == 0:
        stats.leaf_evaluations += 1
        return evaluate(state, root_player)

    if state.to_move == root_player:
        # Maximizing turn.
        best_score = -math.inf
        for move in legal_moves(state):
            child = apply_move(state, move)
            score = _minimax_value(child, remaining_depth - 1, root_player, stats)
            if score > best_score:
                best_score = score
        return best_score

    # Minimizing turn (opponent).
    best_score = math.inf
    for move in legal_moves(state):
        child = apply_move(state, move)
        score = _minimax_value(child, remaining_depth - 1, root_player, stats)
        if score < best_score:
            best_score = score
    return best_score


def minimax_search(state: GameState, depth: int = 3) -> SearchResult:
    """Pick the best move for state.to_move using depth-limited Minimax."""
    if depth < 1:
        raise ValueError("depth must be at least 1")

    start_time = time.perf_counter()
    root_player = state.to_move
    stats = SearchStats(completed_depth=depth)

    # Count the root node.
    stats.nodes_visited += 1

    # Root is already terminal: no move to make, root player has lost.
    if is_terminal(state):
        stats.elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return SearchResult(move=None, score=LOSS_SCORE, stats=stats)

    best_move = None
    best_score = -math.inf

    # Moves come back sorted, so ties are broken the same way every time.
    for move in legal_moves(state):
        child = apply_move(state, move)
        score = _minimax_value(child, depth - 1, root_player, stats)
        if score > best_score:  # strictly better only
            best_score = score
            best_move = move

    stats.elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return SearchResult(move=best_move, score=best_score, stats=stats)