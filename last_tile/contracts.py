"""Frozen data contracts shared across Game Rules, AI Agents, and UI.

Pre-implemented in the initial scaffold so all 4 team members can work
in parallel on Day 1 without merge conflicts.
"""
from __future__ import annotations
from dataclasses import dataclass, field

Move = tuple[int, int]


@dataclass(frozen=True)
class GameState:
    """Immutable snapshot of a Last Tile board configuration."""
    size: int = 5
    positions: tuple[Move, Move] = ((0, 0), (4, 4))
    blocked: frozenset[Move] = field(default_factory=frozenset)
    to_move: int = 0


@dataclass
class SearchStats:
    """Counters populated during a single AI move search."""
    nodes_visited: int = 0
    leaf_evaluations: int = 0
    cutoff_events: int = 0
    elapsed_ms: float = 0.0
    completed_depth: int = 0


@dataclass(frozen=True)
class SearchResult:
    """Standard return object for Hill Climbing, Minimax, and Alpha-Beta."""
    move: Move | None
    score: float
    stats: SearchStats
