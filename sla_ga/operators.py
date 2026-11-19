"""GA parts the engine plugs together: pairing, crossover and mutation.

None of these change the parent array; they only read it.
"""

from abc import ABC, abstractmethod

from sla_ga.config import GAConfig
from sla_ga.types import ChildPair, FitnessArray, Generator, IndexPair, Population, RateChange, Schedule


# Pairing: chooses which best-half parents breed together

class Pairing(ABC):
    """Base class. Every pairing method returns index pairs into the best-half parents."""

    @abstractmethod
    def pair(self, fitness: FitnessArray, n_pairs: int, rng: Generator) -> list[IndexPair]:
        """Return n_pairs (i, j) pairs with i != j.

        Raises:
            ValueError: n_pairs < 1 or fitness has fewer than 2 entries.
        """
        ...


class SoftmaxPairing(Pairing):
    """Default (required). Softmax over fitness gives each parent's chance; redraw j if i == j."""

    def __init__(self, temperature: float) -> None:
        """Store the temperature.

        Raises:
            ValueError: temperature <= 0.
        """
        self._temperature: float
        raise NotImplementedError

    def pair(self, fitness: FitnessArray, n_pairs: int, rng: Generator) -> list[IndexPair]:
        """Draw pairs with probabilities scipy.special.softmax(fitness / temperature);
        if both picks match, redraw the second (up to 10 tries)."""
        raise NotImplementedError


class TournamentPairing(Pairing):
    """Comparison run: each parent is the best of k random picks."""

    def __init__(self, k: int = 3) -> None:
        """Store k.

        Raises:
            ValueError: k < 1.
        """
        self._k: int
        raise NotImplementedError

    def pair(self, fitness: FitnessArray, n_pairs: int, rng: Generator) -> list[IndexPair]:
        """Each pick: k random indices, keep the fittest. Pairs with i != j."""
        raise NotImplementedError


class RandomPairing(Pairing):
    """Comparison run: every parent equally likely."""

    def pair(self, fitness: FitnessArray, n_pairs: int, rng: Generator) -> list[IndexPair]:
        """Uniform random pairs with i != j; fitness is only used for its length."""
        raise NotImplementedError


# Crossover: builds two children from two parents

class Crossover(ABC):
    """Base class. Every crossover method returns two new arrays; the parents are never changed."""

    @abstractmethod
    def cross(self, parent_a: Schedule, parent_b: Schedule, rng: Generator) -> ChildPair:
        """Return (child_1, child_2) as new arrays.

        Raises:
            ValueError: the parents are not both shape (11, 3).
        """
        ...


class SinglePointCrossover(Crossover):
    """Default. Cut row c drawn from 1-10: child 1 = A[:c] + B[c:], child 2 = B[:c] + A[c:]."""

    def cross(self, parent_a: Schedule, parent_b: Schedule, rng: Generator) -> ChildPair:
        """Single-point crossover at an activity boundary."""
        raise NotImplementedError


class UniformCrossover(Crossover):
    """Each activity row comes from A or B at 50/50; child 2 gets the other parent's row."""

    def cross(self, parent_a: Schedule, parent_b: Schedule, rng: Generator) -> ChildPair:
        """Uniform crossover, one coin flip per activity row."""
        raise NotImplementedError


def make_pairing(config: GAConfig) -> Pairing:
    """Build the pairing class named by config.pairing ("softmax", "tournament", "random").

    Raises:
        ValueError: unknown name.
    """
    raise NotImplementedError


def make_crossover(config: GAConfig) -> Crossover:
    """Build the crossover class named by config.crossover ("single_point", "uniform").

    Raises:
        ValueError: unknown name.
    """
    raise NotImplementedError


# Mutation

class Mutator:
    """Holds the current mutation rate and mutates children in place."""

    def __init__(self, rate: float) -> None:
        """Store the rate.

        Raises:
            ValueError: rate not in (0, 1].
        """
        self._rate: float
        raise NotImplementedError

    def mutate(self, children: Population, rng: Generator) -> int:
        """For every room, time and facilitator in every child: with chance rate, replace it
        with a different random value from its range in DOMAIN_SIZES:
        new = (old + rng.integers(1, size)) % size. Changes children in place;
        returns how many genes changed."""
        raise NotImplementedError

    def set_rate(self, rate: float) -> None:
        """Change the rate.

        Raises:
            ValueError: rate not in (0, 1].
        """
        raise NotImplementedError

    def get_rate(self) -> float:
        """The current rate."""
        raise NotImplementedError


class MutationRateTracker:
    """Remembers every mutation rate change, for the log, CSV and GUI chart."""

    def __init__(self) -> None:
        """Start with no entries."""
        self._entries: list[RateChange]
        raise NotImplementedError

    def record(self, generation: int, old: float, new: float, reason: str) -> None:
        """Add one (generation, old rate, new rate, reason) entry."""
        raise NotImplementedError

    def history(self) -> list[RateChange]:
        """A copy of every entry, oldest first."""
        raise NotImplementedError
