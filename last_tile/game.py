"""Problem formulation: board rules, legal moves, transitions, and heuristic (Owner: Member A)."""
from __future__ import annotations

from last_tile.contracts import GameState, Move

TERMINAL_SCORE: float = 10_000.0

KNIGHT_DELTAS: tuple[Move, ...] = (
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
)


def _validate_player(player: int) -> None:
    if player not in (0, 1):
        raise ValueError(f"Invalid player {player!r}; expected 0 or 1.")


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
    """Return sorted tuple of legal knight moves for the specified player."""
    active = state.to_move if player is None else player
    _validate_player(active)

    r0, c0 = state.positions[active]
    occupied = set(state.positions)
    moves: list[Move] = []

    for dr, dc in KNIGHT_DELTAS:
        nr, nc = r0 + dr, c0 + dc
        dest = (nr, nc)
        if (
            0 <= nr < state.size
            and 0 <= nc < state.size
            and dest not in state.blocked
            and dest not in occupied
        ):
            moves.append(dest)

    return tuple(sorted(moves))


def apply_move(state: GameState, move: Move) -> GameState:
    """Validate move, block the moving player's old tile, and switch turns."""
    if move not in legal_moves(state):
        raise ValueError(f"Illegal move {move} for player {state.to_move}.")

    active = state.to_move
    old_pos = state.positions[active]
    new_positions = (
        (move, state.positions[1]) if active == 0 else (state.positions[0], move)
    )

    return GameState(
        size=state.size,
        positions=new_positions,
        blocked=state.blocked | {old_pos},
        to_move=1 - active,
    )


def is_terminal(state: GameState) -> bool:
    """Return True if state.to_move has no legal moves remaining."""
    return len(legal_moves(state)) == 0


def winner(state: GameState) -> int | None:
    """Return winning player index (0 or 1) if terminal, else None."""
    if is_terminal(state):
        return 1 - state.to_move
    return None


def evaluate(state: GameState, root_player: int) -> float:
    """Heuristic h(s, p) = 10 * (my_moves - opp_moves) + (opp_center_dist - my_center_dist)."""
    _validate_player(root_player)
    opp = 1 - root_player

    mobility_diff = len(legal_moves(state, root_player)) - len(legal_moves(state, opp))

    center = (state.size - 1) / 2.0
    my_r, my_c = state.positions[root_player]
    opp_r, opp_c = state.positions[opp]

    my_dist = abs(my_r - center) + abs(my_c - center)
    opp_dist = abs(opp_r - center) + abs(opp_c - center)
    center_diff = opp_dist - my_dist

    return float(10.0 * mobility_diff + center_diff)