"""Mutation rate sweep across seeds (Full Plan Section 9)."""

from sla_ga.config import GAConfig
from sla_ga.types import SweepRow


def run_sweep(rates: list[float], seeds: list[int], config: GAConfig) -> list[SweepRow]:
    """Run the GA for every rate and seed, with every other setting taken from config.

    Writes output/mutation_sweep.csv (rate, seed, final best, final average,
    generations, seconds) and a chart of mean final best against the rate.

    Raises:
        ValueError: rates or seeds is empty, or a rate is not in (0, 1].
    """
    raise NotImplementedError
