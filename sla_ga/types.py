"""Shared type aliases and constants. Import these so every signature reads the same way.

Every alias uses the `type` statement, which Python evaluates lazily. That lets
Listener and Axes name GenerationStats and Matplotlib's Axes without importing
engine.py or Matplotlib when the program runs (no circular import).
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Final

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from matplotlib.axes import Axes as MatplotlibAxes

    from sla_ga.engine import GenerationStats

# Constants: Catalog.validate checks the JSON against these.
N_ACTIVITIES: Final = 11
DOMAIN_SIZES: Final = (9, 6, 10)  # rooms, times, facilitators: the value range of each schedule column

# Schedules and scores
type Schedule = NDArray[np.int8]          # shape (11, 3): room, time, facilitator per activity
type Population = NDArray[np.int8]        # shape (N, 11, 3)
type FitnessArray = NDArray[np.float64]   # shape (N,): one score per schedule
type Generator = np.random.Generator      # the run's random generator (PCG64DXSM)

# Fitness breakdown
type Entry = tuple[str, str, float]       # (rule id, activity or pair, points)
type ViolationCounts = dict[str, int]     # violation name -> count

# GA parts
type IndexPair = tuple[int, int]                     # two parent indices
type ChildPair = tuple[Schedule, Schedule]           # the two children from one crossover
type ParentSet = tuple[Population, FitnessArray]     # best-half parents and their scores
type StopCheck = tuple[bool, str]                    # whether to stop, and why
type RateChange = tuple[int, float, float, str]      # generation, old rate, new rate, reason
type Listener = Callable[[GenerationStats], None]    # called after each generation
type SweepRow = tuple[float, int, float, float, int, float]  # rate, seed, final best, final average, generations, seconds

# Scoring values
type ScoreTable = dict[str, float]                   # one section of scoring.json, e.g. room_size["big"] = -0.2
type Band = tuple[float, float]                      # (minimum enrollment / capacity rate, points), optional rule O1
type LoadExceptions = dict[int, int]                 # facilitator index -> exempt below this count (Tyler: 2)
type TimePreferences = dict[int, dict[int, float]]   # facilitator index -> time index -> points, optional rule O2

# GUI
type Axes = MatplotlibAxes                           # a chart area the gui/charts.py functions draw on
