"""Command-line entry point.

    python cli.py [--seed 42] [--pop 252] ...      run the GA ("run" is the default command)
    python cli.py sweep --rates ... --seeds ...    mutation rate sweep
"""

import argparse
import sys
from collections.abc import Callable

from sla_ga.config import GAConfig
from sla_ga.engine import GenerationStats
from sla_ga.report import GROUP_OPTIONS, SHOW_OPTIONS, SORT_OPTIONS

COMMANDS = ("run", "sweep")
PAIRINGS = ("softmax", "tournament", "random")
CROSSOVERS = ("single_point", "uniform")

# --rules name -> GAConfig switch it turns on
RULE_FLAGS = {
    "scaling": "room_size_scaling",
    "timepref": "time_preferences",
    "equipment": "equipment",
}


def _comma_list[T](item_type: Callable[[str], T]) -> Callable[[str], list[T]]:
    """Make an argparse type that turns "a,b,c" into a non-empty list of item_type."""

    def parse(text: str) -> list[T]:
        parts = [part.strip() for part in text.split(",") if part.strip()]
        if not parts:
            raise argparse.ArgumentTypeError("expected a comma-separated list, got nothing")
        try:
            return [item_type(part) for part in parts]
        except ValueError as error:
            raise argparse.ArgumentTypeError(str(error)) from None

    return parse


def _rule_name(text: str) -> str:
    """argparse item type for --rules: accept only the names in RULE_FLAGS."""
    if text not in RULE_FLAGS:
        raise ValueError(f"unknown rule {text!r}; choose from {', '.join(RULE_FLAGS)}")
    return text


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Read the command-line flags (README "Running").

    Returns a Namespace whose names match GAConfig fields where they overlap:
        command          "run" or "sweep"
        population_size, temperature, pairing, crossover, max_generations, auto_halve
        rules            list of RULE_FLAGS names (empty when none)
        run only:   seed, mutation_rate, show, sort_by, group_by
        sweep only: rates (list[float]), seeds (list[int])

    Only checks that values parse and come from their allowed set. Ranges
    (population >= 250, rate in (0, 1], ...) are checked by make_config via GAConfig.validate.

    Raises:
        SystemExit: a flag is unknown or a value cannot be parsed (argparse prints the reason).
    """
    args_list = list(sys.argv[1:] if argv is None else argv)
    if not args_list or args_list[0] not in COMMANDS:
        args_list.insert(0, "run")  # "python cli.py --seed 1" means "run --seed 1"

    defaults = GAConfig()

    # GA settings shared by both commands
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--pop", dest="population_size", type=int, default=defaults.population_size,
                        help="population size, at least 250 and a multiple of 4 (default %(default)s)")
    shared.add_argument("--temperature", type=float, default=defaults.temperature,
                        help="softmax temperature, greater than 0 (default %(default)s)")
    shared.add_argument("--pairing", choices=PAIRINGS, default=defaults.pairing,
                        help="how parents are paired (default %(default)s)")
    shared.add_argument("--crossover", choices=CROSSOVERS, default=defaults.crossover,
                        help="crossover method (default %(default)s)")
    shared.add_argument("--max-gen", dest="max_generations", type=int, default=defaults.max_generations,
                        help="generation cap, at least 100 (default %(default)s)")
    shared.add_argument("--auto-halve", action="store_true",
                        help="halve the mutation rate instead of stopping")
    shared.add_argument("--rules", type=_comma_list(_rule_name), default=[],
                        help=f"optional rules, comma-separated: {', '.join(RULE_FLAGS)}")

    parser = argparse.ArgumentParser(prog="cli.py", description="SLA activity scheduler (genetic algorithm).")
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", parents=[shared], help="run the GA once (default)")
    run.add_argument("--seed", type=int, default=defaults.seed,
                     help="random seed (default: random, printed and saved)")
    run.add_argument("--mutation", dest="mutation_rate", type=float, default=defaults.mutation_rate,
                     help="mutation rate, greater than 0 and at most 1 (default %(default)s)")
    run.add_argument("--show", choices=SHOW_OPTIONS, default="first6",
                     help="activities to print (default %(default)s)")
    run.add_argument("--sort", dest="sort_by", choices=SORT_OPTIONS, default="time",
                     help="schedule order (default %(default)s)")
    run.add_argument("--group", dest="group_by", choices=GROUP_OPTIONS, default="none",
                     help="schedule grouping (default %(default)s)")

    sweep = commands.add_parser("sweep", parents=[shared], help="mutation rate sweep across seeds")
    sweep.add_argument("--rates", type=_comma_list(float), required=True,
                       help="mutation rates, comma-separated, e.g. 0.01,0.005,0.0025")
    sweep.add_argument("--seeds", type=_comma_list(int), required=True,
                       help="seeds, comma-separated, e.g. 1,2,3,4,5")

    return parser.parse_args(args_list)


def make_config(args: argparse.Namespace) -> GAConfig:
    """Build a GAConfig from the parsed flags and validate it.

    Copy the Namespace names that match GAConfig fields; seed and mutation_rate
    only exist for "run", so a sweep keeps the GAConfig defaults for them.
    Turn on the GAConfig switch named in RULE_FLAGS for each entry in args.rules.

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
