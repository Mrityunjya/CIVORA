from dataclasses import dataclass


@dataclass
class EvacuationOrigin:
    origin_id: str
    name: str
    latitude: float
    longitude: float
    population: int