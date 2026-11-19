"""Fixed problem data: activities, rooms, times and facilitators."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Catalog:
    """All facts from sla_catalog.json, as lists in index order. Never changes after loading."""

    # Activities (index 0-10)
    activity_names: list[str]
    enrollment: list[int]
    activity_equipment: list[set[str]]
    sla101: list[int]                 # activity indices of SLA101A, SLA101B
    sla191: list[int]                 # activity indices of SLA191A, SLA191B

    # Rooms (index 0-8)
    room_names: list[str]
    capacity: list[int]
    building: list[str]
    room_equipment: list[set[str]]

    # Times (index 0-5)
    hours: list[int]                  # 10-15, so a slot gap is a subtraction
    time_names: list[str]

    # Facilitators (index 0-9)
    facilitator_names: list[str]

    # Per activity: facilitator indices from its "preferred" and "other" lists
    _preferred: list[set[int]]
    _other: list[set[int]]

    @classmethod
    def load(cls, path: Path) -> Catalog:
        """Read the JSON, turn names into index lists, build a Catalog, call validate() and return it.

        Raises:
            FileNotFoundError: the file does not exist.
            ValueError: a key is missing or a name in a preferred/other/sla list is unknown.
        """
        raise NotImplementedError

    def validate(self) -> None:
        """Raise ValueError on bad data; warn (warnings.warn) on a facilitator in both lists.

        - every capacity and enrollment is > 0
        - no duplicate room or activity names
        - counts match DOMAIN_SIZES and N_ACTIVITIES
        - hours are in ascending order
        - SLA449 lists Zeldin as preferred and other: warn, don't raise
        """
        raise NotImplementedError

    def facilitator_category(self, activity: int, facilitator: int) -> str:
        """Return "preferred", "other" or "unlisted" (preferred checked first).

        Raises:
            IndexError: activity or facilitator is out of range.
        """
        raise NotImplementedError
