"""Every GA setting in one validated object."""

from dataclasses import dataclass


@dataclass
class GAConfig:
    """All run settings. Allowed values are in Shared Definitions 2."""

    catalog_path: str = "data/sla_catalog.json"
    scoring_path: str = "data/scoring.json"
    population_size: int = 252
    seed: int | None = None
    mutation_rate: float = 0.01
    temperature: float = 1.0
    pairing: str = "softmax"              # "softmax" | "tournament" | "random"
    crossover: str = "single_point"       # "single_point" | "uniform"
    max_generations: int = 1000
    min_generations: int = 100
    improvement_threshold: float = 1.0    # percent
    auto_halve: bool = False
    min_mutation_rate: float = 0.0003125  # 0.01 / 32
    halve_wait: int = 20

    # Optional fitness rules
    room_size_scaling: bool = False
    time_preferences: bool = False
    equipment: bool = False

    def validate(self) -> None:
        """Raise ValueError if any setting is outside its allowed range.

        - population_size >= 250 and a multiple of 4
        - 0 < mutation_rate <= 1 and 0 < min_mutation_rate <= mutation_rate
        - temperature > 0
        - min_generations >= 100 and max_generations >= min_generations
        - improvement_threshold > 0, halve_wait >= 1
        - pairing and crossover are one of the allowed strings
        """
        raise NotImplementedError
