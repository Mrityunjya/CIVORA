from backend.models.evacuation import EvacuationOrigin


EVACUATION_ORIGINS = [

    EvacuationOrigin(
        origin_id="ZONE_A",
        name="Residential Zone A",
        latitude=13.0060,
        longitude=80.2560,
        population=1200,
    ),

    EvacuationOrigin(
        origin_id="ZONE_B",
        name="Residential Zone B",
        latitude=13.0100,
        longitude=80.2575,
        population=850,
    ),

    EvacuationOrigin(
        origin_id="ZONE_C",
        name="Commercial Zone C",
        latitude=13.0130,
        longitude=80.2610,
        population=1500,
    ),

]