# Last Tile — AI Game-Playing Agent

> **Status:** Initial Scaffold — Shared contracts (`contracts.py`) and UI shell are ready; member modules contain `TODO` stubs.

**Last Tile** is a 5×5 King-Move Isolation game built for the **AI with Python** course project. It implements and compares three direct move-selecting AI algorithms:
1. **Steepest-Ascent Hill Climbing** (`last_tile/ai/hill_climbing.py`) — Local search agent (1-ply heuristic neighbor evaluation)
2. **Minimax Search** (`last_tile/ai/minimax.py`) — Unpruned depth-limited adversarial search
3. **Alpha-Beta Pruning** (`last_tile/ai/alphabeta.py`) — Pruned adversarial search returning the exact same optimal move as Minimax in far fewer nodes

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run unit tests (scaffold smoke tests pass out of the box)
python -m unittest discover -s tests -v

# 3. Launch browser UI
streamlit run streamlit_app.py

# 4. Run algorithm benchmarks (after Member A-D modules are implemented)
python benchmark.py
```

## Four-Person Split

| Member | Branch | Owned Files | Role |
| :--- | :--- | :--- | :--- |
| **Member A** | `feature/game` | `last_tile/game.py`, `tests/test_game.py` | Problem formulation (board rules, legal moves, constraints) & heuristic `evaluate()` |
| **Member B** | `feature/minimax` | `last_tile/ai/minimax.py`, `tests/test_minimax.py` | Algorithm 2: Depth-limited Minimax search |
| **Member C** | `feature/alphabeta` | `last_tile/ai/alphabeta.py`, `tests/test_alphabeta.py`, `benchmark.py` | Algorithm 3: Alpha-Beta pruning & 3-algorithm benchmark script |
| **Member D** | `feature/ui-hillclimb` | `last_tile/ai/hill_climbing.py`, `tests/test_hill_climbing.py`, `streamlit_app.py` | Algorithm 1: Hill Climbing agent & Streamlit UI |

See [`AI_BRIEF.md`](./AI_BRIEF.md) for full details and AI handoff instructions.
