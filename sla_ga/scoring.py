"""Every point value and threshold from scoring.json."""

from dataclasses import dataclass
from pathlib import Path

from sla_ga.catalog import Catalog
from sla_ga.types import Band, LoadExceptions, ScoreTable, TimePreferences


@dataclass(frozen=True)
class Scoring:
    """Point values for the fitness rules. Loaded once, never changes during a run.

    Example: scoring.room_size["big"] is -0.2.
    """

    room_conflict: float                 # F1
    room_size: ScoreTable                # F2a-F2d
    facilitator_preference: ScoreTable   # F3
    facilitator_same_slot: ScoreTable    # F4
    facilitator_load: ScoreTable         # F5a, F5b
    consecutive_slots: ScoreTable        # F6
    section_pairs: ScoreTable            # P1-P4
    cross_pairs: ScoreTable              # P5, P6
    far_buildings: set[str]              # Roman, Beach

    # From "optional"
    room_size_bands: list[Band]          # O1, highest minimum rate first
    room_size_too_small: float           # O1
    equipment: ScoreTable                # O3

    _min_activities_exceptions: LoadExceptions   # facilitator index -> exempt below this count
    _time_preferences: TimePreferences           # facilitator index -> time index -> points (O2)

    @classmethod
    def load(cls, path: Path, catalog: Catalog) -> Scoring:
        """Read the JSON, turn facilitator and time names into indices, build a Scoring,
        call validate(catalog) and return it.

        Raises:
            FileNotFoundError: the file does not exist.
            ValueError: a key is missing or a facilitator or time name is not in the catalog.
        """
        raise NotImplementedError

    def validate(self, catalog: Catalog) -> None:
        """Raise ValueError if a value is not a number, a far building is not in the catalog,
        or room_size_bands are not in descending order of minimum rate."""
        raise NotImplementedError

    def is_underloaded(self, facilitator: int, count: int) -> bool:
        """True when the -0.4 underload penalty applies.

        count < facilitator_load["min_activities"] (3), unless count is below the
        facilitator's exception value (Tyler: no penalty at 1, penalty at 2).

        Raises:
            ValueError: count < 1.
        """
        raise NotImplementedError

    def is_far_building(self, building: str) -> bool:
        """True if building is in far_buildings (Roman, Beach)."""
        raise NotImplementedError

    def time_preference(self, facilitator: int, time: int) -> float:
        """Points for this facilitator at this time slot; 0.0 if none listed (optional rule O2)."""
        raise NotImplementedError
