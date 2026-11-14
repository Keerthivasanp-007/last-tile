"""Algorithm 1: Steepest-Ascent Hill Climbing local search agent (Member D)."""
from __future__ import annotations
import math
import time
from last_tile.contracts import GameState, Move, SearchResult, SearchStats
from last_tile import game

WIN_SCORE: float = 10_000.0
LOSS_SCORE: float = -10_000.0

_KNIGHT_OFFSETS: tuple[Move, ...] = (
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
)


def _legal_moves(state: GameState, player: int | None = None) -> tuple[Move, ...]:
    p = state.to_move if player is None else player
    try:
        return game.legal_moves(state, p)
    except NotImplementedError:
        r0, c0 = state.positions[p]
        moves: list[Move] = []
        for dr, dc in _KNIGHT_OFFSETS:
            nr, nc = r0 + dr, c0 + dc
            if 0 <= nr < state.size and 0 <= nc < state.size:
                dest = (nr, nc)
                if dest not in state.blocked and dest not in state.positions:
                    moves.append(dest)
        return tuple(sorted(moves))


def _apply_move(state: GameState, move: Move) -> GameState:
    try:
        return game.apply_move(state, move)
    except NotImplementedError:
        if move not in _legal_moves(state):
            raise ValueError(f"Illegal move: {move}")
        old_pos = state.positions[state.to_move]
        new_blocked = state.blocked | {old_pos}
        new_positions = (
            (move, state.positions[1])
            if state.to_move == 0
            else (state.positions[0], move)
        )
        return GameState(
            size=state.size,
            positions=new_positions,
            blocked=new_blocked,
            to_move=1 - state.to_move,
        )


def _is_terminal(state: GameState) -> bool:
    try:
        return game.is_terminal(state)
    except NotImplementedError:
        return len(_legal_moves(state)) == 0


def _winner(state: GameState) -> int | None:
    try:
        return game.winner(state)
    except NotImplementedError:
        return (1 - state.to_move) if _is_terminal(state) else None


def _evaluate(state: GameState, root_player: int) -> float:
    try:
        return game.evaluate(state, root_player)
    except NotImplementedError:
        opp = 1 - root_player
        mob_diff = len(_legal_moves(state, root_player)) - len(_legal_moves(state, opp))
        center = (state.size - 1) / 2.0
        pr, pc = state.positions[root_player]
        or_, oc = state.positions[opp]
        p_dist = abs(pr - center) + abs(pc - center)
        opp_dist = abs(or_ - center) + abs(oc - center)
        return float(10.0 * mob_diff + (opp_dist - p_dist))


def hill_climbing_search(state: GameState) -> SearchResult:
    """Pick the best immediate move using Steepest-Ascent Hill Climbing.

    Evaluates all 1-step legal neighbor states from `state.to_move`'s perspective
    and climbs directly to the neighbor with the highest heuristic value.
    """
    start_time = time.perf_counter()
    root_player = state.to_move
    stats = SearchStats(completed_depth=1)

    # Count the current (root) state.
    stats.nodes_visited += 1

    # If the root is already terminal, the active player has no legal moves and loses.
    if _is_terminal(state):
        stats.elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return SearchResult(move=None, score=LOSS_SCORE, stats=stats)

    best_move: Move | None = None
    best_score: float = -math.inf

    # Evaluate every immediate neighbor state in deterministic sorted move order.
    for move in _legal_moves(state):
        neighbor = _apply_move(state, move)
        stats.nodes_visited += 1
        stats.leaf_evaluations += 1

        if _is_terminal(neighbor):
            score = WIN_SCORE if _winner(neighbor) == root_player else LOSS_SCORE
        else:
            score = _evaluate(neighbor, root_player)

        if score > best_score:
            best_score = score
            best_move = move

    stats.elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return SearchResult(move=best_move, score=best_score, stats=stats)