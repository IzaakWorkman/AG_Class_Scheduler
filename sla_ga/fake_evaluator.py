"""Stand-in for FitnessEvaluator so the engine can be built and run before the real rules exist.

Score = how many of a schedule's 33 values match a fixed target schedule (best possible: 33).
If the engine works, best fitness climbs toward 33 over the generations.
Replaced by the real FitnessEvaluator in task 3.2.
"""

import numpy as np

from sla_ga.catalog import Catalog
from sla_ga.config import GAConfig
from sla_ga.fitness import VIOLATION_KEYS
from sla_ga.scoring import Scoring
from sla_ga.types import DOMAIN_SIZES, N_ACTIVITIES, Entry, FitnessArray, Population, Schedule, ViolationCounts

TARGET_SEED = 0  # fixed, so the target is the same in every run


class FakeEvaluator:
    """Same public methods as FitnessEvaluator, with a made-up score."""

    def __init__(self, catalog: Catalog, scoring: Scoring, config: GAConfig) -> None:
        """Store the arguments (unused, kept so it is a drop-in swap) and build the target schedule."""
        self._catalog = catalog
        self._scoring = scoring
        self._config = config

        rng = np.random.default_rng(TARGET_SEED)
        columns = [rng.integers(0, size, N_ACTIVITIES) for size in DOMAIN_SIZES]
        self._target: Schedule = np.stack(columns, axis=1).astype(np.int8)  # shape (11, 3)

    def breakdown(self, schedule: Schedule) -> list[Entry]:
        """A single entry holding the whole fake score."""
        return [("FAKE", "schedule", self.score(schedule))]

    def score(self, schedule: Schedule) -> float:
        """Number of values that match the target schedule (0-33)."""
        if schedule.shape != self._target.shape:
            raise ValueError(f"schedule must have shape {self._target.shape}, got {schedule.shape}")
        return float(np.sum(schedule == self._target))

    def score_all(self, population: Population) -> FitnessArray:
        """score() for every schedule at once; returns an array of N floats."""
        if population.ndim != 3 or population.shape[1:] != self._target.shape:
            raise ValueError(f"population must have shape (N, 11, 3), got {population.shape}")
        return np.sum(population == self._target, axis=(1, 2)).astype(np.float64)

    def violations(self, schedule: Schedule) -> ViolationCounts:
        """All 8 violation keys, every count 0 (the fake score has no rules to break)."""
        return dict.fromkeys(VIOLATION_KEYS, 0)
