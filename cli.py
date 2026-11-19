"""Command-line entry point.

    python cli.py [--seed 42] [--pop 252] ...      run the GA
    python cli.py sweep --rates ... --seeds ...    mutation rate sweep
"""

import argparse

from sla_ga.config import GAConfig
from sla_ga.engine import GenerationStats


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read the command-line flags (README "Running"), including the print options
    (--show, --sort, --group) and the sweep command (--rates, --seeds).

    Raises:
        SystemExit: a flag is unknown or a value cannot be parsed (argparse's own behaviour).
    """
    raise NotImplementedError


def make_config(args: argparse.Namespace) -> GAConfig:
    """Build a GAConfig from the parsed flags and validate it.

    Raises:
        ValueError: a setting is outside its allowed range (from GAConfig.validate).
    """
    raise NotImplementedError


def print_generation(stats: GenerationStats) -> None:
    """Listener: print one line - generation, best, average, worst, improvement %, mutation rate."""
    raise NotImplementedError


def plot_history(history: list[GenerationStats]) -> None:
    """plotext line chart of best, average and worst fitness over generations (required chart)."""
    raise NotImplementedError


def main() -> None:
    """Parse args; run the sweep, or load the catalog and scoring, build the engine and
    Reporter (Shared Definitions 6), add listeners, run, print the schedule and the chart."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
