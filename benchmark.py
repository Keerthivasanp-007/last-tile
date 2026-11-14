"""Benchmark: Hill Climbing vs Minimax vs Alpha-Beta (Member C).

Part 1 - search efficiency on 10 sample states -> results/benchmark_summary.csv
         and results/algorithm_comparison.png
Part 2 - solution quality: 10 games, Alpha-Beta (depth 3) vs Hill Climbing,
         swapping starting sides.

Run:  python benchmark.py
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

from last_tile.contracts import GameState
from last_tile.game import apply_move, is_terminal, legal_moves, new_game, winner
from last_tile.ai.alphabeta import alphabeta_search
from last_tile.ai.hill_climbing import hill_climbing_search
from last_tile.ai.minimax import minimax_search

RESULTS_DIR = Path(__file__).parent / "results"
NUM_STATES = 10
NUM_GAMES = 10
SEED = 7
DEPTHS = (2, 3, 4)


def sample_states(n: int = NUM_STATES, seed: int = SEED) -> list[GameState]:
    """n reproducible non-terminal mid-game states (2-11 plies from the start)."""
    rng = random.Random(seed)
    states: list[GameState] = []
    for k in range(n):
        target = 2 + (k % 10)
        while True:
            s = new_game()
            for _ in range(target):
                if is_terminal(s):
                    break
                s = apply_move(s, rng.choice(legal_moves(s)))
            if not is_terminal(s):
                states.append(s)
                break
    return states


def part1_efficiency(states: list[GameState]) -> list[dict]:
    configs = [("Hill Climbing", "-", lambda s: hill_climbing_search(s))]
    for d in DEPTHS:
        configs.append(("Minimax", d, lambda s, d=d: minimax_search(s, d)))
    for d in DEPTHS:
        configs.append(("Alpha-Beta", d, lambda s, d=d: alphabeta_search(s, d)))

    rows = []
    for name, depth, fn in configs:
        res = [fn(s).stats for s in states]
        avg = lambda attr: sum(getattr(r, attr) for r in res) / len(res)
        rows.append({
            "algorithm": name,
            "depth": depth,
            "avg_elapsed_ms": round(avg("elapsed_ms"), 4),
            "avg_nodes_visited": round(avg("nodes_visited"), 2),
            "avg_leaf_evaluations": round(avg("leaf_evaluations"), 2),
            "avg_cutoff_events": round(avg("cutoff_events"), 2),
        })

    RESULTS_DIR.mkdir(exist_ok=True)
    csv_path = RESULTS_DIR / "benchmark_summary.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {csv_path}")
    return rows


def plot(rows: list[dict]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = [r["algorithm"] if r["depth"] == "-" else f'{r["algorithm"]}\nd={r["depth"]}'
              for r in rows]
    colors = ["tab:green" if r["algorithm"] == "Hill Climbing"
              else "tab:blue" if r["algorithm"] == "Minimax" else "tab:orange"
              for r in rows]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, key, title in (
        (axes[0], "avg_nodes_visited", "Average nodes visited"),
        (axes[1], "avg_elapsed_ms", "Average time (ms)"),
    ):
        ax.bar(range(len(rows)), [r[key] for r in rows], color=colors)
        ax.set_xticks(range(len(rows)))
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_title(title)
        ax.set_yscale("log")
        ax.grid(axis="y", alpha=0.3)
    fig.suptitle("Last Tile: search efficiency over 10 sample states (log scale)")
    fig.tight_layout()
    path = RESULTS_DIR / "algorithm_comparison.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved {path}")


def play_game(ab_side: int, depth: int = 3) -> int | None:
    """Alpha-Beta controls ab_side, Hill Climbing the other. Returns winner."""
    s = new_game()
    while not is_terminal(s):
        if s.to_move == ab_side:
            move = alphabeta_search(s, depth).move
        else:
            move = hill_climbing_search(s).move
        s = apply_move(s, move)
    return winner(s)


def part2_quality() -> None:
    ab_wins = hc_wins = 0
    print(f"\nPart 2: Alpha-Beta (depth 3) vs Hill Climbing, {NUM_GAMES} games")
    for g in range(NUM_GAMES):
        ab_side = g % 2  # alternate: Alpha-Beta moves first on even games
        w = play_game(ab_side)
        if w == ab_side:
            ab_wins += 1
        else:
            hc_wins += 1
        print(f"  Game {g + 1:2d}: Alpha-Beta as P{ab_side} -> "
              f"{'Alpha-Beta' if w == ab_side else 'Hill Climbing'} wins")
    print(f"Record: Alpha-Beta {ab_wins} - {hc_wins} Hill Climbing")


def main() -> None:
    states = sample_states()
    print(f"Part 1: search efficiency on {len(states)} sample states")
    rows = part1_efficiency(states)
    header = f'{"Algorithm":<14}{"Depth":>6}{"ms":>10}{"Nodes":>12}{"Leaves":>12}{"Cutoffs":>10}'
    print(header)
    for r in rows:
        print(f'{r["algorithm"]:<14}{str(r["depth"]):>6}{r["avg_elapsed_ms"]:>10.3f}'
              f'{r["avg_nodes_visited"]:>12.1f}{r["avg_leaf_evaluations"]:>12.1f}'
              f'{r["avg_cutoff_events"]:>10.1f}')
    plot(rows)
    part2_quality()


if __name__ == "__main__":
    main()
