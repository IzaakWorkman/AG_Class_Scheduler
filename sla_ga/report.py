"""Writes every output file for one run into output/run_<YYYYMMDD-HHMMSS>_seed<seed>/."""

from pathlib import Path
from typing import TextIO

from sla_ga.catalog import Catalog
from sla_ga.engine import GenerationStats, RunResult
from sla_ga.fitness import VIOLATION_KEYS
from sla_ga.types import Schedule

CSV_NAME = "fitness_history.csv"
LOG_NAME = "run.log"
BEST_NAME = "best_schedule.txt"

# One CSV row per generation (Shared Definitions 5).
CSV_COLUMNS: tuple[str, ...] = (
    "generation", "timestamp", "best", "average", "worst",
    "improvement_pct", "mutation_rate", *VIOLATION_KEYS,
)

# Allowed format_schedule arguments (Shared Definitions 3).
SHOW_OPTIONS = ("first6", "all")
SORT_OPTIONS = ("time", "activity")
GROUP_OPTIONS = ("none", "building", "facilitator")


class Reporter:
    """Listener that writes the CSV, the log and best_schedule.txt for one run."""

    def __init__(self, run_dir: Path, catalog: Catalog) -> None:
        """Create run_dir, open the CSV (write the header) and the log file."""
        self._run_dir: Path
        self._catalog: Catalog
        self._csv_file: TextIO
        self._log_file: TextIO
        raise NotImplementedError

    def on_generation(self, stats: GenerationStats) -> None:
        """Append one CSV row (improvement_pct blank at generation 0) and one
        timestamped log line with the best schedule; flush both."""
        raise NotImplementedError

    def format_schedule(self, schedule: Schedule, show: str, sort_by: str, group_by: str) -> str:
        """Text table of the schedule, built from a ScheduleView.

        Columns: Activity, Time, Room, Building, Facilitator, Enrollment / Capacity.

        Raises:
            ValueError: show, sort_by or group_by is not one of its allowed options.
        """
        raise NotImplementedError

    def write_best(self, result: RunResult) -> Path:
        """Write best_schedule.txt: best fitness, seed, settings, stop reason,
        the full schedule sorted by time and its violation counts. Return its path."""
        raise NotImplementedError

    def close(self) -> None:
        """Flush and close the CSV and log files. Safe to call twice."""
        raise NotImplementedError
