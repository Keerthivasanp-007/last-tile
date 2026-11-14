"""Problem formulation: board rules, legal moves, transitions, and heuristic (Owner: Member A)."""
from __future__ import annotations
from last_tile.contracts import GameState, Move

TERMINAL_SCORE: float = 10_000.0


def new_game(size: int = 5) -> GameState:
    """Create the initial 5x5 game state with Player 0 at (0,0) and Player 1 at (size-1,size-1)."""
    if size < 2:
        raise ValueError("Board size must be at least 2.")
    return GameState(
        size=size,
        positions=((0, 0), (size - 1, size - 1)),
        blocked=frozenset(),
        to_move=0,
    )


def legal_moves(state: GameState, player: int | None = None) -> tuple[Move, ...]:
    """Return sorted tuple of legal 1-step king moves for the specified player."""
    raise NotImplementedError("TODO(Member A): Implement legal_moves in last_tile/game.py")


def apply_move(state: GameState, move: Move) -> GameState:
    """Validate move, block the moving player's old tile, and switch turns."""
    raise NotImplementedError("TODO(Member A): Implement apply_move in last_tile/game.py")


def is_terminal(state: GameState) -> bool:
    """Return True if state.to_move has no legal moves remaining."""
    raise NotImplementedError("TODO(Member A): Implement is_terminal in last_tile/game.py")


def winner(state: GameState) -> int | None:
    """Return winning player index (0 or 1) if terminal, else None."""
    raise NotImplementedError("TODO(Member A): Implement winner in last_tile/game.py")


def evaluate(state: GameState, root_player: int) -> float:
    """Heuristic h(s, p) = 10 * (my_moves - opp_moves) + (opp_center_dist - my_center_dist)."""
    raise NotImplementedError("TODO(Member A): Implement evaluate in last_tile/game.py")
