"""Optional fitness rules (assignment "OPTIONAL interesting constraints").

Plain functions so they can be written without touching fitness.py.
FitnessEvaluator._optional_rules calls each one only if its GAConfig switch is on.
Each returns (rule, who, points) entries like the base rules, non-zero points only.
"""

from sla_ga.catalog import Catalog
from sla_ga.scoring import Scoring
from sla_ga.types import Entry, Schedule


def room_size_scaling_rows(s: Schedule, catalog: Catalog, scoring: Scoring) -> list[Entry]:
    """O1, replaces F2. Rate = enrollment / capacity: over 1.0 -> scoring.room_size_too_small (-1.0),
    else the first of scoring.room_size_bands whose minimum the rate reaches
    (83-100% +0.8, 75-83% +0.5, 67-75% +0.2, 50-67% -0.3, under 50% -0.6)."""
    raise NotImplementedError


def time_preference_rows(s: Schedule, catalog: Catalog, scoring: Scoring) -> list[Entry]:
    """O2: scoring.time_preference(facilitator, time) for each activity
    (Glen, Banks, Tyler and Singer likes and dislikes)."""
    raise NotImplementedError


def equipment_rows(s: Schedule, catalog: Catalog, scoring: Scoring) -> list[Entry]:
    """O3: compare the activity's needs with the room's equipment.
    All met +0.2, some met -0.1, none met -0.3. Activities with no needs are skipped."""
    raise NotImplementedError
