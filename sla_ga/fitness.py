"""Appendix A fitness rules. Every point value comes from Scoring.

Each rule method returns (rule, who, points) entries, non-zero points only.
Rule ids are from Full Plan Section 7. "who" is one activity name, or two names
joined by "+" in catalog order for pair rules ("SLA101A+SLA191B").
"""

from sla_ga.catalog import Catalog
from sla_ga.config import GAConfig
from sla_ga.scoring import Scoring
from sla_ga.types import Entry, FitnessArray, Population, Schedule, ViolationCounts

# violations() returns these keys, in this order (Shared Definitions 5).
VIOLATION_KEYS: tuple[str, ...] = (
    "room_conflicts",
    "facilitator_double_booked",
    "facilitator_overloaded",
    "facilitator_underloaded",
    "room_too_small",
    "room_too_big",
    "non_listed_facilitator",
    "special_rule",
)


class FitnessEvaluator:
    """Scores schedules with the Appendix A rubric, plus the optional rules that are switched on."""

    def __init__(self, catalog: Catalog, scoring: Scoring, config: GAConfig) -> None:
        """Store the catalog, the scoring values and the config (for the optional rule switches)."""
        raise NotImplementedError

    def breakdown(self, schedule: Schedule) -> list[Entry]:
        """Call every rule method and return all their entries in one list."""
        raise NotImplementedError

    def score(self, schedule: Schedule) -> float:
        """Total fitness: the sum of the points in breakdown(schedule)."""
        raise NotImplementedError

    def score_all(self, population: Population) -> FitnessArray:
        """score() for every schedule; returns an array of N floats."""
        raise NotImplementedError

    def violations(self, schedule: Schedule) -> ViolationCounts:
        """Count penalty entries from breakdown. Always all VIOLATION_KEYS, 0 when none.

        room_conflicts: F1 | facilitator_double_booked: F4 at -0.2 | facilitator_overloaded: F5a
        facilitator_underloaded: F5b | room_too_small: F2a | room_too_big: F2b, F2c
        non_listed_facilitator: F3 at -0.1 | special_rule: P2, P4, P6 at -0.25, every -0.4 mismatch
        """
        raise NotImplementedError

    # Rule methods, one per rule group

    def _room_conflicts(self, s: Schedule) -> list[Entry]:
        """F1: -0.5 once for each activity sharing a room and time with another."""
        raise NotImplementedError

    def _room_size(self, s: Schedule) -> list[Entry]:
        """F2: capacity < enrollment -0.5, > 3x -0.4, > 1.5x -0.2, else +0.3 (strict, in that order).
        Skipped when config.room_size_scaling is on (O1 replaces it)."""
        raise NotImplementedError

    def _facilitator_preference(self, s: Schedule) -> list[Entry]:
        """F3: preferred +0.5, other +0.2, unlisted -0.1, via catalog.facilitator_category."""
        raise NotImplementedError

    def _facilitator_same_slot(self, s: Schedule) -> list[Entry]:
        """F4: +0.2 if the facilitator has only this activity at this time, -0.2 if more."""
        raise NotImplementedError

    def _facilitator_total_load(self, s: Schedule) -> list[Entry]:
        """F5a: -0.5 per activity if the facilitator has more than 4.
        F5b: -0.4 per activity when scoring.is_underloaded(f, count)."""
        raise NotImplementedError

    def _facilitator_consecutive(self, s: Schedule) -> list[Entry]:
        """F6: +0.5 per pair of a facilitator's activities in back-to-back slots,
        then a separate -0.4 entry if exactly one of the two rooms is Roman or Beach."""
        raise NotImplementedError

    def _sla_section_pairs(self, s: Schedule) -> list[Entry]:
        """P1-P4: SLA101 A/B and SLA191 A/B. More than 4 hours apart +0.5, same slot -0.5."""
        raise NotImplementedError

    def _sla_cross_pairs(self, s: Schedule) -> list[Entry]:
        """P5, P6 on all 4 (SLA101, SLA191) pairs: 1 hour apart +0.5 (then a separate -0.4
        Roman/Beach entry), 2 hours apart +0.25, same slot -0.25."""
        raise NotImplementedError

    def _optional_rules(self, s: Schedule) -> list[Entry]:
        """Call the optional_rules.py functions whose config switch is on."""
        raise NotImplementedError
