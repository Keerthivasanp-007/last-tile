# LAST TILE — Minimal AI Handoff Brief & Specification

**Course:** AI with Python | **Team Size:** 4 Students | **Target Python:** 3.10+

> **How to use this file with your AI coding model:**
> Upload this `.md` file (along with the files you own) to your AI assistant and say:
> *"I am **Member [A / B / C / D]** working on the Last Tile AI project. Follow this brief strictly. Only write or modify the files assigned to my role, preserve all function signatures in `contracts.py` and `game.py`, and give me commands to verify my tests."*

---

## 1. Project Overview & The 3 Course Algorithms

**Last Tile** is a 5×5 turn-based Isolation board game implemented in Python with a minimal **Streamlit** browser UI (`streamlit_app.py`) and a single performance comparison script (`benchmark.py`).

All three AI algorithms act directly as **game-playing agents** that take a `GameState` and return a `SearchResult` (chosen move, score, visited states, pruning cutoffs, and execution time):

| # | Algorithm | Course Syllabus Category | How It Chooses a Move in Last Tile | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Steepest-Ascent Hill Climbing** | Local Search | Evaluates all immediate legal next states $s'$ using the heuristic $h(s', p)$ and climbs directly to the highest-scoring neighbor (fast, explores at most 8 states per turn, no lookahead). | Member D |
| **2** | **Minimax Search** | Adversarial Search | Explores the full game tree up to depth $d$ plies assuming an optimal opponent (maximizing at own turns, minimizing at opponent turns). | Member B |
| **3** | **Alpha-Beta Pruning** | Adversarial Search | Explores the same depth-$d$ game tree while pruning branches where $\beta \le \alpha$, returning the **exact same move and score as Minimax** in far fewer explored states and less time. | Member C |

---

## 2. Problem Formulation & Exact Game Rules (Requirement 2)

1. **Initial State (`new_game`):**
   - 5×5 grid using 0-indexed `(row, col)` coordinates from `(0, 0)` to `(4, 4)`.
   - Player `0` starts at `(0, 0)` and moves first (`to_move = 0`). Player `1` starts at `(4, 4)`.
   - `blocked` starts as an empty `frozenset`.
2. **State Space & Legal Actions (`legal_moves`):**
   - On a turn, the active player moves **1 step in any of the 8 king directions** ($\Delta r \in \{-1, 0, 1\}, \Delta c \in \{-1, 0, 1\}$, excluding $(0, 0)$).
   - **Constraints:** A destination `(r, c)` is legal if and only if:
     - $0 \le r < \text{size}$ and $0 \le c < \text{size}$ (inside board boundaries)
     - `(r, c)` is **not** in `state.blocked`
     - `(r, c)` is **not** occupied by either player (`state.positions[0]` or `state.positions[1]`)
   - Always return legal moves sorted in ascending `(row, col)` order so all algorithms break ties identically.
3. **Transition Model (`apply_move`):**
   - Validates that `move` is in `legal_moves(state)` (raises `ValueError` otherwise).
   - Adds the moving player's **old position** to `blocked` (the tile falls away / is permanently blocked).
   - Updates the moving player's position to `move` and switches `to_move` to `1 - state.to_move`.
4. **Terminal / Goal State (`is_terminal`, `winner`):**
   - A state is **terminal** when `legal_moves(state)` is empty for `state.to_move`.
   - The player with no legal moves loses; the other player (`1 - state.to_move`) wins.
   - Terminal utility from `root_player`'s perspective: **`+10_000.0`** if `winner(state) == root_player`, **`-10_000.0`** if `winner(state) != root_player`.
5. **Heuristic Evaluation Function (`evaluate`):**
   - Evaluated at non-terminal states from `root_player`'s perspective (`p = root_player`, `opp = 1 - root_player`):
     $$h(s, p) = 10.0 \times \bigl(|\text{legal\_moves}(s, p)| - |\text{legal\_moves}(s, \text{opp})|\bigr) + \bigl(d_{\text{center}}(\text{pos}[\text{opp}]) - d_{\text{center}}(\text{pos}[p])\bigr)$$
   - Where $d_{\text{center}}(r, c) = |r - c_0| + |c - c_0|$ is the Manhattan distance to the board center $c_0 = \frac{\text{size} - 1}{2}$.
   - Rewards having more legal moves than the opponent (**Mobility**) and staying closer to the center of the board (**Center Control**). Strictly antisymmetric: `evaluate(s, 0) == -evaluate(s, 1)`.

---

## 3. Minimal Repository Layout & Four-Person Split

Only **13 files total**—no extra config folders, JSON fixtures, or offline training pipelines:

```text
last-tile/
├── README.md                  # Quickstart & run commands
├── AI_BRIEF.md                # This file — share with all 4 teammates
├── requirements.txt           # streamlit, matplotlib, pytest
├── .gitignore                 # Standard Python ignores
├── streamlit_app.py           # [Member D] Minimal playable browser UI
├── benchmark.py               # [Member C] CLI script comparing all 3 algorithms
├── last_tile/
│   ├── __init__.py
│   ├── contracts.py           # [PRE-BUILT IN SCAFFOLD] Shared dataclasses
│   ├── game.py                # [Member A] Board rules, transitions, & heuristic
│   └── ai/
│       ├── __init__.py
│       ├── hill_climbing.py   # [Member D] Algorithm 1: Steepest-Ascent Hill Climbing
│       ├── minimax.py         # [Member B] Algorithm 2: Depth-Limited Minimax
│       └── alphabeta.py       # [Member C] Algorithm 3: Alpha-Beta Pruning
├── results/
│   └── .gitkeep               # Output folder for benchmark CSV & plot
└── tests/
    ├── test_scaffold.py       # [PRE-BUILT] Passing smoke tests
    ├── test_game.py           # [Member A] Game rules & heuristic tests
    ├── test_minimax.py        # [Member B] Minimax search tests
    ├── test_alphabeta.py      # [Member C] Alpha-Beta & equivalence tests
    └── test_hill_climbing.py  # [Member D] Hill Climbing agent tests
```

| Member | Branch | Owned Files | Viva Explanation Focus |
| :--- | :--- | :--- | :--- |
| **Member A** | `feature/game` | `last_tile/game.py`, `tests/test_game.py` | Problem formulation (state space, actions, constraints, terminal test) & heuristic $h(s, p)$ |
| **Member B** | `feature/minimax` | `last_tile/ai/minimax.py`, `tests/test_minimax.py` | Adversarial search tree, maximizing/minimizing recursion, depth cutoff |
| **Member C** | `feature/alphabeta` | `last_tile/ai/alphabeta.py`, `tests/test_alphabeta.py`, `benchmark.py` | $\alpha$-$\beta$ pruning condition ($\beta \le \alpha$), equivalence with Minimax, performance metrics |
| **Member D** | `feature/ui-hillclimb` | `last_tile/ai/hill_climbing.py`, `tests/test_hill_climbing.py`, `streamlit_app.py` | Steepest-Ascent Hill Climbing local search, local optima limitation, Streamlit UI |

---

## 4. Shared Contracts (`last_tile/contracts.py` — Already Implemented)

`last_tile/contracts.py` is **already complete in the initial scaffold** so all 4 members can work in parallel immediately:

```python
from dataclasses import dataclass, field

Move = tuple[int, int]

@dataclass(frozen=True)
class GameState:
    size: int = 5
    positions: tuple[Move, Move] = ((0, 0), (4, 4))
    blocked: frozenset[Move] = field(default_factory=frozenset)
    to_move: int = 0

@dataclass
class SearchStats:
    nodes_visited: int = 0
    leaf_evaluations: int = 0
    cutoff_events: int = 0
    elapsed_ms: float = 0.0
    completed_depth: int = 0

@dataclass(frozen=True)
class SearchResult:
    move: Move | None
    score: float
    stats: SearchStats
```

---

## 5. Exact Task Specifications per Member

### Member A — Problem Formulation & Heuristic (`last_tile/game.py` & `tests/test_game.py`)
1. `new_game(size: int = 5) -> GameState` (already provided in scaffold).
2. `legal_moves(state: GameState, player: int | None = None) -> tuple[Move, ...]`:
   - If `player is None`, use `state.to_move`. Validate `player in (0, 1)`.
   - Return a sorted tuple of all legal 1-step king moves `(r, c)` from `state.positions[player]` that are inside the `size × size` grid, not in `state.blocked`, and not in `state.positions`.
3. `apply_move(state: GameState, move: Move) -> GameState`:
   - Raise `ValueError` if `move not in legal_moves(state)`.
   - Return a new `GameState` with the active player's old position added to `state.blocked`, active player moved to `move`, and `to_move = 1 - state.to_move`.
4. `is_terminal(state: GameState) -> bool`:
   - Return `len(legal_moves(state)) == 0`.
5. `winner(state: GameState) -> int | None`:
   - Return `1 - state.to_move` if `is_terminal(state)` is `True`, else `None`.
6. `evaluate(state: GameState, root_player: int) -> float`:
   - Validate `root_player in (0, 1)`.
   - Compute mobility difference `len(legal_moves(state, root_player)) - len(legal_moves(state, 1 - root_player))` and center-distance difference as defined in Section 2. Return `float(10.0 * mobility_diff + center_diff)`.
7. **Tests (`tests/test_game.py`):** Test corner/center move counts, blocking of previous tile, rejection of illegal moves, terminal win detection, and `evaluate(s, 0) == -evaluate(s, 1)`.

### Member B — Algorithm 2: Minimax Search (`last_tile/ai/minimax.py` & `tests/test_minimax.py`)
1. `minimax_search(state: GameState, depth: int = 3) -> SearchResult`:
   - Require `depth >= 1` (else raise `ValueError`). Fix `root_player = state.to_move`.
   - Track runtime with `time.perf_counter()` and initialize `SearchStats(completed_depth=depth)`.
   - Increment `stats.nodes_visited += 1` on every node visited (including root and leaves).
   - **Terminal check first:** If `is_terminal(curr_state)`, return `+10_000.0` if `winner(curr_state) == root_player` else `-10_000.0` (with `move=None` if the root itself is terminal).
   - **Depth cutoff (`rem_depth == 0`):** Increment `stats.leaf_evaluations += 1` and return `evaluate(curr_state, root_player)`.
   - **Recursion:** Iterate over `legal_moves(curr_state)` in sorted order. Maximize when `curr_state.to_move == root_player` (update best move on strict improvement `score > best_score`); minimize when `curr_state.to_move != root_player` (`score < best_score`).
2. **Tests (`tests/test_minimax.py`):** Verify legal move returned, `nodes_visited > 1`, terminal win in 1 ply is chosen, and `move=None` on a terminal root.

### Member C — Algorithm 3: Alpha-Beta Pruning & Benchmarks (`last_tile/ai/alphabeta.py`, `tests/test_alphabeta.py`, `benchmark.py`)
1. `alphabeta_search(state: GameState, depth: int = 3) -> SearchResult`:
   - Same parameters, terminal check, leaf evaluation, node counting, and strict tie-breaking as `minimax_search`.
   - Maintain `alpha = -math.inf` and `beta = math.inf`.
   - Update `alpha = max(alpha, best_score)` at maximizing nodes and `beta = min(beta, best_score)` at minimizing nodes.
   - When `beta <= alpha` and **at least one remaining sibling move has not been explored**, increment `stats.cutoff_events += 1` and `break`.
2. **Tests (`tests/test_alphabeta.py`):** Verify that on multiple mid-game states at depths 1–3, `alphabeta_search` returns the **exact same `move` and `score`** as `minimax_search` while visiting fewer or equal nodes (`alphabeta.stats.nodes_visited <= minimax.stats.nodes_visited`).
3. **Benchmark Script (`benchmark.py`):**
   - Part 1 (Search Efficiency): Run `hill_climbing_search`, `minimax_search` (depths 2, 3, 4), and `alphabeta_search` (depths 2, 3, 4) on 10 sample game states; save average `elapsed_ms`, `nodes_visited`, `leaf_evaluations`, and `cutoff_events` to `results/benchmark_summary.csv` and plot a comparison chart to `results/algorithm_comparison.png`.
   - Part 2 (Solution Quality / Win Rate): Simulate 10 automated games of **Alpha-Beta (depth 3) vs. Hill Climbing** (swapping starting sides) and print the win/loss record.

### Member D — Algorithm 1: Hill Climbing & Streamlit UI (`last_tile/ai/hill_climbing.py`, `tests/test_hill_climbing.py`, `streamlit_app.py`)
1. `hill_climbing_search(state: GameState) -> SearchResult`:
   - Fix `root_player = state.to_move`. Start timer and `SearchStats(completed_depth=1, nodes_visited=1)` (counting the current state).
   - If `is_terminal(state)`, return `SearchResult(move=None, score=-10_000.0, stats=stats)`.
   - Generate all legal moves `moves = legal_moves(state)`. For each `m` in `moves`:
     - Generate neighbor `next_state = apply_move(state, m)`.
     - Increment `stats.nodes_visited += 1` and `stats.leaf_evaluations += 1`.
     - Score `next_state`: if `is_terminal(next_state)` (opponent is immediately trapped!), score is `+10_000.0`; otherwise `evaluate(next_state, root_player)`.
     - Keep the move with the highest strict score improvement (`val > best_score`).
   - Record `elapsed_ms` and return `SearchResult(move=best_move, score=best_score, stats=stats)`.
2. **Tests (`tests/test_hill_climbing.py`):** Verify legal move selection, `nodes_visited == 1 + len(legal_moves(state))`, and immediate winning move selection when available.
3. **Streamlit UI (`streamlit_app.py`):**
   - Sidebar: Select AI Agent (`Alpha-Beta Pruning`, `Minimax`, or `Hill Climbing (Local Search)`), Search Depth slider (`1`–`4`, disabled when Hill Climbing is selected), Human Side (`Player 0` or `Player 1`), and `New Game` button.
   - Main Board: 5×5 clickable button grid showing Player 0 (`🔵 P0`), Player 1 (`🔴 P1`), blocked tiles (`⬛`), and highlighted legal moves (`🟢`), plus an explicit **`Make AI Move`** button and a live metrics row showing `Move Chosen`, `Nodes Visited`, `Pruning Cutoffs`, and `Time (ms)`.

---

## 6. Commands to Run & Verify

```bash
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Run all unit tests (works with both unittest and pytest)
python -m unittest discover -s tests -v
python -m pytest -v

# 3. Start the Streamlit interface
python -m streamlit run streamlit_app.py

# 4. Run algorithm comparison benchmarks (once A, B, C, D are implemented)
python benchmark.py
```