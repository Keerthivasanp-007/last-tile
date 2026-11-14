"""Algorithm 3: Depth-limited Alpha-Beta Pruning (Member C).

Returns the exact same move and score as minimax_search, but prunes branches
once beta <= alpha, so it visits fewer (or equally many) nodes.
"""
from __future__ import annotations

import math
import time

from last_tile.contracts import GameState, SearchResult, SearchStats
from last_tile.game import apply_move, evaluate, is_terminal, legal_moves, winner


def alphabeta_search(state: GameState, depth: int = 3) -> SearchResult:
    if depth < 1:
        raise ValueError("depth must be >= 1")

    start = time.perf_counter()
    root_player = state.to_move
    stats = SearchStats(completed_depth=depth)

    def terminal_score(s: GameState) -> float:
        return 10_000.0 if winner(s) == root_player else -10_000.0

    def search(s: GameState, rem_depth: int, alpha: float, beta: float) -> float:
        stats.nodes_visited += 1

        if is_terminal(s):
            return terminal_score(s)
        if rem_depth == 0:
            stats.leaf_evaluations += 1
            return evaluate(s, root_player)

        moves = legal_moves(s)
        maximizing = s.to_move == root_player
        best_score = -math.inf if maximizing else math.inf

        for i, move in enumerate(moves):
            score = search(apply_move(s, move), rem_depth - 1, alpha, beta)
            if maximizing:
                if score > best_score:
                    best_score = score
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)

            if beta <= alpha:
                if i < len(moves) - 1:  # at least one sibling left unexplored
                    stats.cutoff_events += 1
                    break
        return best_score

    # Root (always a maximizing node for root_player)
    stats.nodes_visited += 1
    if is_terminal(state):
        stats.elapsed_ms = (time.perf_counter() - start) * 1000.0
        return SearchResult(move=None, score=terminal_score(state), stats=stats)

    alpha, beta = -math.inf, math.inf
    best_move = None
    best_score = -math.inf
    moves = legal_moves(state)
    for i, move in enumerate(moves):
        score = search(apply_move(state, move), depth - 1, alpha, beta)
        if score > best_score:  # strict improvement => same tie-breaking as minimax
            best_score, best_move = score, move
        alpha = max(alpha, best_score)
        if beta <= alpha:
            if i < len(moves) - 1:
                stats.cutoff_events += 1
                break

    stats.elapsed_ms = (time.perf_counter() - start) * 1000.0
    return SearchResult(move=best_move, score=best_score, stats=stats)
