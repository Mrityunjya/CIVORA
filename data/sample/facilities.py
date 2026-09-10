from backend.models.facility import EmergencyFacility


FACILITIES = [

    EmergencyFacility(
        facility_id="H001",
        name="Facility Alpha",
        facility_type="hospital",
        latitude=13.0069,
        longitude=80.2555,
    ),

    EmergencyFacility(
        facility_id="H002",
        name="Facility Beta",
        facility_type="hospital",
        latitude=13.0140,
        longitude=80.2580,
    ),

    EmergencyFacility(
        facility_id="H003",
        name="Facility Gamma",
        facility_type="emergency_center",
        latitude=13.0025,
        longitude=80.2620,
    ),

]