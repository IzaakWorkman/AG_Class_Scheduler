"""Random populations, range checks and a readable view of one schedule.

A schedule is an (11, 3) int8 array: one row per activity, columns [room, time, facilitator].
"""

from dataclasses import dataclass

from sla_ga.catalog import Catalog
from sla_ga.types import Generator, Population, Schedule


def random_population(rng: Generator, size: int) -> Population:
    """Return a (size, 11, 3) int8 array with every room, time and facilitator
    picked at random within DOMAIN_SIZES.

    Raises:
        ValueError: size < 1.
    """
    raise NotImplementedError


def check_population(pop: Population) -> None:
    """Raise ValueError if pop is not (N, 11, 3) or any value is outside its range
    in DOMAIN_SIZES (rooms 0-8, times 0-5, facilitators 0-9)."""
    raise NotImplementedError


@dataclass(frozen=True)
class ActivityRow:
    """One activity of a schedule, with names instead of indices."""

    activity: str
    time: str
    room: str
    building: str
    facilitator: str
    enrollment: int
    capacity: int


class ScheduleView:
    """Read-only wrapper around one finished schedule, for printing and the GUI."""

    def __init__(self, schedule: Schedule, catalog: Catalog) -> None:
        """Store a copy of the schedule and the catalog.

        Raises:
            ValueError: schedule is not (11, 3) or a value is out of range.
        """
        raise NotImplementedError

    def rows(self) -> list[ActivityRow]:
        """One ActivityRow per activity, in catalog order."""
        raise NotImplementedError

    def activity(self, name: str) -> ActivityRow:
        """The row for one activity, e.g. view.activity("SLA101A").room.

        Raises:
            KeyError: name is not an activity in the catalog.
        """
        raise NotImplementedError
