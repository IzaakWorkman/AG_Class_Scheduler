"""The generation loop. The engine prints nothing; it sends a GenerationStats to its listeners."""

import threading
from dataclasses import dataclass
from datetime import datetime

from sla_ga.catalog import Catalog
from sla_ga.config import GAConfig
from sla_ga.fitness import FitnessEvaluator
from sla_ga.operators import Crossover, MutationRateTracker, Mutator, Pairing
from sla_ga.scoring import Scoring
from sla_ga.types import (
    FitnessArray, Generator, IndexPair, Listener, ParentSet, Population, Schedule,
    StopCheck, ViolationCounts,
)


@dataclass(frozen=True)
class GenerationStats:
    """One record per generation, sent to every listener."""

    generation: int
    best: float
    average: float
    worst: float
    improvement_pct: float | None   # None at generation 0
    mutation_rate: float
    best_schedule: Schedule         # a copy, shape (11, 3)
    violations: ViolationCounts     # of the best schedule
    timestamp: datetime


@dataclass(frozen=True)
class RunResult:
    """What run() returns when the run ends."""

    best_schedule: Schedule
    best_fitness: float
    generations: int
    stop_reason: str
    history: list[GenerationStats]
    seed: int


class GAEngine:
    """Owns the population and runs the GA loop.

    Next population = best half (unchanged) + mutated children, so its size never changes.
    """

    def __init__(self, config: GAConfig, catalog: Catalog, scoring: Scoring) -> None:
        """Validate the config; pick a seed if none was given
        (np.random.SeedSequence().entropy % 2**32); make the generator
        (np.random.Generator(np.random.PCG64DXSM(seed))); build the evaluator, pairing,
        crossover, mutator and tracker; create and score generation 0.
        Generation 0's stats are sent by run(), because listeners are added after __init__.

        Raises:
            ValueError: the config is invalid (from config.validate).
        """
        self._config: GAConfig
        self._catalog: Catalog
        self._scoring: Scoring
        self.seed: int
        self._rng: Generator
        self._evaluator: FitnessEvaluator
        self._pairing: Pairing
        self._crossover: Crossover
        self._mutator: Mutator
        self._tracker: MutationRateTracker
        self._population: Population
        self._fitness: FitnessArray
        self._generation: int
        self._listeners: list[Listener]
        self._paused: threading.Event   # set = paused
        self._stopped: threading.Event  # set = stop requested
        raise NotImplementedError

    def add_listener(self, func: Listener) -> None:
        """Register a function to call with each GenerationStats.

        Raises:
            TypeError: func is not callable.
        """
        raise NotImplementedError

    def step(self) -> GenerationStats:
        """Run one generation, in this order: _keep_best_half -> pair -> _make_children ->
        mutate children -> score children -> combine -> build GenerationStats and send it
        to every listener. Returns the stats."""
        raise NotImplementedError

    def run(self) -> RunResult:
        """Send generation 0's stats to the listeners, then call step() until _should_stop()
        is true (or stop() was called). Waits while paused, checking the flags between
        generations. Returns a RunResult."""
        raise NotImplementedError

    def set_mutation_rate(self, rate: float) -> None:
        """Called by the GUI: applies from the next generation and is recorded in the tracker.

        Raises:
            ValueError: rate not in (0, 1].
        """
        raise NotImplementedError

    def pause(self) -> None:
        """Ask run() to wait before the next generation."""
        raise NotImplementedError

    def resume(self) -> None:
        """Let a paused run() continue."""
        raise NotImplementedError

    def stop(self) -> None:
        """Ask run() to finish after the current generation (also releases a pause)."""
        raise NotImplementedError

    def _keep_best_half(self) -> ParentSet:
        """Sort by fitness; return copies of the top N/2 schedules and their scores."""
        raise NotImplementedError

    def _make_children(self, parents: Population, pairs: list[IndexPair]) -> Population:
        """crossover.cross on every pair; stack both children into one new (N/2, 11, 3) array."""
        raise NotImplementedError

    def _improvement_pct(self, prev_avg: float, avg: float) -> float:
        """(avg - prev_avg) / max(abs(prev_avg), 0.000001) * 100."""
        raise NotImplementedError

    def _should_stop(self) -> StopCheck:
        """(True, reason) when generation >= min_generations and improvement <
        improvement_threshold, or at max_generations. Calls _maybe_halve first, which
        can keep the run going."""
        raise NotImplementedError

    def _maybe_halve(self) -> bool:
        """If auto_halve is on and the run would stop, halve the rate instead (not below
        min_mutation_rate, at most once per halve_wait generations), record it in the
        tracker and return True."""
        raise NotImplementedError
