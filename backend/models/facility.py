from dataclasses import dataclass


@dataclass
class EmergencyFacility:
    facility_id: str
    name: str
    facility_type: str
    latitude: float
    longitude: float