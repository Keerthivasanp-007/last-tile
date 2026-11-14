"""Minimal, centered interactive UI for Last Tile — Knight-Move Isolation AI (Owner: Member D)."""
from __future__ import annotations
import csv
from pathlib import Path
import time
import streamlit as st
from last_tile.contracts import GameState, Move, SearchResult
from last_tile import game
from last_tile.ai import alphabeta, hill_climbing, minimax

st.set_page_config(
    page_title="Last Tile — Knight Isolation",
    layout="centered",
    initial_sidebar_state="expanded",
)

KNIGHT_OFFSETS = (
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
)


# ---------------------------------------------------------------------------
# Fallback helpers so the board is playable before Member A merges game.py
# ---------------------------------------------------------------------------
def safe_legal_moves(state: GameState, player: int | None = None) -> tuple[Move, ...]:
    p = state.to_move if player is None else player
    try:
        return game.legal_moves(state, p)
    except NotImplementedError:
        r0, c0 = state.positions[p]
        moves: list[Move] = []
        for dr, dc in KNIGHT_OFFSETS:
            nr, nc = r0 + dr, c0 + dc
            if 0 <= nr < state.size and 0 <= nc < state.size:
                dest = (nr, nc)
                if dest not in state.blocked and dest not in state.positions:
                    moves.append(dest)
        return tuple(sorted(moves))


def safe_apply_move(state: GameState, move: Move) -> GameState:
    try:
        return game.apply_move(state, move)
    except NotImplementedError:
        if move not in safe_legal_moves(state):
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


def safe_is_terminal(state: GameState) -> bool:
    try:
        return game.is_terminal(state)
    except NotImplementedError:
        return len(safe_legal_moves(state)) == 0


def safe_winner(state: GameState) -> int | None:
    try:
        return game.winner(state)
    except NotImplementedError:
        return (1 - state.to_move) if safe_is_terminal(state) else None


def run_ai_agent(state: GameState, agent_spec: str) -> tuple[SearchResult | None, str | None]:
    try:
        if agent_spec == "hill_climbing":
            return hill_climbing.hill_climbing_search(state), None
        if agent_spec.startswith("minimax:"):
            depth = int(agent_spec.split(":")[1])
            return minimax.minimax_search(state, depth=depth), None
        if agent_spec.startswith("alphabeta:"):
            depth = int(agent_spec.split(":")[1])
            return alphabeta.alphabeta_search(state, depth=depth), None
        return None, f"Unknown agent: {agent_spec}"
    except NotImplementedError as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
AGENT_OPTIONS = [
    "Human",
    "hill_climbing",
    "minimax:2",
    "minimax:3",
    "minimax:4",
    "alphabeta:2",
    "alphabeta:3",
    "alphabeta:4",
]

AGENT_LABELS = {
    "Human": "Human",
    "hill_climbing": "Hill Climbing (Local)",
    "minimax:2": "Minimax (Depth 2)",
    "minimax:3": "Minimax (Depth 3)",
    "minimax:4": "Minimax (Depth 4)",
    "alphabeta:2": "Alpha-Beta (Depth 2)",
    "alphabeta:3": "Alpha-Beta (Depth 3)",
    "alphabeta:4": "Alpha-Beta (Depth 4)",
}


def reset_match(board_size: int = 5) -> None:
    st.session_state.game_state = game.new_game(size=board_size)
    st.session_state.last_status = "Match started — Player 1 (Red) moves first."
    st.session_state.ai_error = None


if "game_state" not in st.session_state:
    reset_match(5)
if "last_status" not in st.session_state:
    st.session_state.last_status = "Match started — Player 1 (Red) moves first."
if "ai_error" not in st.session_state:
    st.session_state.ai_error = None

# ---------------------------------------------------------------------------
# Sidebar: Controls + Benchmarks toggle
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Last Tile")
    view_mode = st.radio(
        "Navigation",
        options=["Play Game", "Benchmarks"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("---")

    board_size = st.selectbox(
        "Board Size",
        options=[5, 7],
        index=0 if st.session_state.game_state.size == 5 else 1,
        format_func=lambda s: f"{s} × {s}",
    )
    if board_size != st.session_state.game_state.size:
        reset_match(board_size)
        st.rerun()

    p1_agent = st.selectbox(
        "Player 1 (Red)",
        options=AGENT_OPTIONS,
        index=0,
        format_func=lambda k: AGENT_LABELS[k],
    )
    p2_agent = st.selectbox(
        "Player 2 (Blue)",
        options=AGENT_OPTIONS,
        index=0,
        format_func=lambda k: AGENT_LABELS[k],
    )

    ai_delay_ms = st.slider(
        "AI Move Delay (ms)",
        min_value=0,
        max_value=800,
        value=150,
        step=50,
    )

    if st.button("New Game", use_container_width=True):
        reset_match(board_size)
        st.rerun()

# ---------------------------------------------------------------------------
# CSS: Centered fixed-width square board
# ---------------------------------------------------------------------------
TILE_PX = 76 if st.session_state.game_state.size == 5 else 58
GAP_PX = 6
BOARD_PX = st.session_state.game_state.size * TILE_PX + (st.session_state.game_state.size - 1) * GAP_PX

st.markdown(
    f"""
    <style>
    /* Center the main app block and match its inner width to the board */
    .main .block-container {{
        max-width: {BOARD_PX + 48}px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding: 2rem 24px !important;
    }}

    /* Force each row of columns to exact board width and centered */
    div[data-testid="stHorizontalBlock"] {{
        width: {BOARD_PX}px !important;
        margin: 0 auto {GAP_PX}px auto !important;
        gap: {GAP_PX}px !important;
    }}
    div[data-testid="stColumn"],
    div[data-testid="column"] {{
        width: {TILE_PX}px !important;
        min-width: {TILE_PX}px !important;
        max-width: {TILE_PX}px !important;
        flex: 0 0 {TILE_PX}px !important;
        padding: 0px !important;
    }}

    div[data-testid="stVerticalBlock"],
    div[data-testid="stElementContainer"],
    div.element-container,
    div.stMarkdown,
    div.stButton {{
        gap: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }}

    .board-tile {{
        width: {TILE_PX}px;
        height: {TILE_PX}px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        user-select: none;
    }}
    .tile-empty {{
        background-color: #262b36;
        border: 1px solid #363d4d;
    }}
    .tile-blocked {{
        background-color: #12151c;
        border: 1px solid #1e222d;
        color: #3b4254;
        font-size: 18px;
        font-weight: 700;
    }}
    .tile-occupied {{
        background-color: #1e2330;
        border: 1px solid #363d4d;
    }}

    .token-p1 {{
        width: {TILE_PX - 20}px;
        height: {TILE_PX - 20}px;
        border-radius: 50%;
        background: #ef4444;
        border: 2px solid #fca5a5;
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 10px rgba(239, 68, 68, 0.45);
    }}
    .token-p2 {{
        width: {TILE_PX - 20}px;
        height: {TILE_PX - 20}px;
        border-radius: 50%;
        background: #3b82f6;
        border: 2px solid #93c5fd;
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.45);
    }}

    div.stButton > button[kind="primary"] {{
        width: {TILE_PX}px !important;
        height: {TILE_PX}px !important;
        min-height: {TILE_PX}px !important;
        max-height: {TILE_PX}px !important;
        margin: 0px !important;
        padding: 0px !important;
        border-radius: 8px !important;
        background-color: #22c55e !important;
        border: 2px solid #4ade80 !important;
        color: transparent !important;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.25) !important;
    }}
    div.stButton > button[kind="primary"]:hover {{
        background-color: #16a34a !important;
        border-color: #86efac !important;
    }}

    .status-banner {{
        width: {BOARD_PX}px;
        margin: 0 auto 12px auto;
        background-color: #1e2330;
        border: 1px solid #363d4d;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
        font-size: 16px;
        font-weight: 600;
        color: #f3f4f6;
        box-sizing: border-box;
    }}
    .stats-footer {{
        width: {BOARD_PX}px;
        margin: 8px auto 0 auto;
        background-color: #161922;
        border: 1px solid #262b36;
        border-radius: 8px;
        padding: 10px 14px;
        font-family: monospace;
        font-size: 12.5px;
        color: #9ca3af;
        text-align: center;
        box-sizing: border-box;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Main View
# ---------------------------------------------------------------------------
if view_mode == "Benchmarks":
    st.subheader("Algorithm Benchmarks")
    csv_path = Path("results/benchmark_summary.csv")
    img_path = Path("results/algorithm_comparison.png")
    if csv_path.exists():
        with csv_path.open("r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        st.table(rows)
    else:
        st.info("Run `python benchmark.py` once the AI modules are implemented to view benchmark results here.")
    if img_path.exists():
        st.image(str(img_path))
else:
    state: GameState = st.session_state.game_state
    terminal = safe_is_terminal(state)
    win_idx = safe_winner(state)
    active_agent = p1_agent if state.to_move == 0 else p2_agent

    if terminal:
        winner_text = "Player 1 (Red) Wins!" if win_idx == 0 else "Player 2 (Blue) Wins!"
        st.markdown(f'<div class="status-banner">🏆 {winner_text}</div>', unsafe_allow_html=True)
    elif active_agent == "Human":
        turn_dot = "🔴 Player 1 (Red)" if state.to_move == 0 else "🔵 Player 2 (Blue)"
        st.markdown(f'<div class="status-banner">{turn_dot} — Click a green tile</div>', unsafe_allow_html=True)
    else:
        turn_dot = "🔴 Player 1" if state.to_move == 0 else "🔵 Player 2"
        st.markdown(
            f'<div class="status-banner">{turn_dot} ({AGENT_LABELS[active_agent]}) thinking...</div>',
            unsafe_allow_html=True,
        )

    if st.session_state.ai_error:
        st.warning(
            f"`{active_agent}` is not implemented yet. Switch to **Human** in the sidebar to play."
        )

    legal_set = (
        set(safe_legal_moves(state))
        if (not terminal and active_agent == "Human")
        else set()
    )

    for r in range(state.size):
        row_cols = st.columns(state.size)
        for c in range(state.size):
            pos = (r, c)
            with row_cols[c]:
                if pos == state.positions[0]:
                    st.markdown(
                        '<div class="board-tile tile-occupied"><div class="token-p1">♞</div></div>',
                        unsafe_allow_html=True,
                    )
                elif pos == state.positions[1]:
                    st.markdown(
                        '<div class="board-tile tile-occupied"><div class="token-p2">♞</div></div>',
                        unsafe_allow_html=True,
                    )
                elif pos in state.blocked:
                    st.markdown('<div class="board-tile tile-blocked">✕</div>', unsafe_allow_html=True)
                elif pos in legal_set:
                    if st.button(" ", key=f"cell_{r}_{c}", type="primary"):
                        p_num = state.to_move + 1
                        old_r, old_c = state.positions[state.to_move]
                        st.session_state.game_state = safe_apply_move(state, pos)
                        st.session_state.ai_error = None
                        st.session_state.last_status = f"P{p_num} moved ({old_r},{old_c}) → ({r},{c})"
                        st.rerun()
                else:
                    st.markdown('<div class="board-tile tile-empty"></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="stats-footer">{st.session_state.last_status}</div>', unsafe_allow_html=True)

    state = st.session_state.game_state
    active_agent = p1_agent if state.to_move == 0 else p2_agent
    if not safe_is_terminal(state) and active_agent != "Human" and st.session_state.ai_error is None:
        if ai_delay_ms > 0:
            time.sleep(ai_delay_ms / 1000.0)
        res, err = run_ai_agent(state, active_agent)
        if err is not None:
            st.session_state.ai_error = err
            st.rerun()
        elif res is not None and res.move is not None:
            p_num = state.to_move + 1
            old_r, old_c = state.positions[state.to_move]
            nr, nc = res.move
            st.session_state.game_state = safe_apply_move(state, res.move)
            st.session_state.last_status = (
                f"P{p_num} ({active_agent}): ({old_r},{old_c}) → ({nr},{nc}) | "
                f"nodes: {res.stats.nodes_visited} | cutoffs: {res.stats.cutoff_events} | "
                f"{res.stats.elapsed_ms:.1f}ms"
            )
            st.rerun()