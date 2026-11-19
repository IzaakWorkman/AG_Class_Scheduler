"""Drawing functions for the GUI tabs. Each one draws on the Matplotlib axis it is given, nothing else."""

from sla_ga.catalog import Catalog
from sla_ga.engine import GenerationStats
from sla_ga.types import Axes, RateChange, Schedule, ViolationCounts


def draw_fitness(ax: Axes, history: list[GenerationStats], rates: list[RateChange]) -> None:
    """Best, average and worst fitness lines over generations,
    with the mutation rate as a step line on a second axis."""
    raise NotImplementedError


def draw_course_load(ax: Axes, schedule: Schedule, catalog: Catalog) -> None:
    """Bar chart of activities per facilitator, with lines at the 3 and 4 limits."""
    raise NotImplementedError


def draw_room_utilization(ax: Axes, schedule: Schedule, catalog: Catalog) -> None:
    """Pie chart of activity slots used per room."""
    raise NotImplementedError


def draw_violations(ax: Axes, counts: ViolationCounts) -> None:
    """Pie chart of constraint violations by type (zero counts left out)."""
    raise NotImplementedError
