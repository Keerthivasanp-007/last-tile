"""Minimal Streamlit interface for Last Tile (Owner: Member D)."""
from __future__ import annotations
import streamlit as st
from last_tile.contracts import GameState
from last_tile import game

st.set_page_config(page_title="Last Tile — AI Project", layout="centered")

st.title("Last Tile — 5×5 Isolation AI")
st.warning(
    "Scaffold only — game rules and AI algorithms are not yet implemented. "
    "See `AI_BRIEF.md` for Member A, B, C, and D tasks."
)

if "game_state" not in st.session_state:
    st.session_state.game_state = game.new_game(size=5)

state: GameState = st.session_state.game_state

with st.sidebar:
    st.header("Match Settings")
    algo = st.selectbox(
        "AI Algorithm",
        ["Alpha-Beta Pruning", "Minimax", "Hill Climbing (Local Search)"],
    )
    depth = st.slider(
        "Search Depth (plies)",
        min_value=1,
        max_value=4,
        value=3,
        disabled=(algo == "Hill Climbing (Local Search)"),
    )
    if st.button("New Game", use_container_width=True):
        st.session_state.game_state = game.new_game(size=5)
        st.rerun()

st.subheader("Initial 5×5 Board Preview")
for r in range(state.size):
    cols = st.columns(state.size)
    for c in range(state.size):
        pos = (r, c)
        if pos == state.positions[0]:
            label = "🔵 P0"
        elif pos == state.positions[1]:
            label = "🔴 P1"
        elif pos in state.blocked:
            label = "⬛"
        else:
            label = f"{r},{c}"
        cols[c].button(label, key=f"cell_{r}_{c}", disabled=True, use_container_width=True)

st.caption(
    "TODO(Member D): Connect interactive legal-move clicks, explicit 'Make AI Move' button, "
    "and SearchStats diagnostics once Member A–C modules are implemented."
)
