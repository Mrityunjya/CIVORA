from dataclasses import dataclass


@dataclass
class Incident:
    incident_id: str
    incident_type: str
    node: int
    severity: str = "high"