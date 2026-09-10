from dataclasses import dataclass


@dataclass
class InterventionResult:
    intervention_id: str
    name: str
    description: str
    reachable_origins: int
    blocked_origins: int
    affected_population: int
    total_additional_time_s: float
    total_additional_distance_m: float
    score: float
    recommended: bool = False