from backend.services.routing import route_from_coordinates


def rank_facilities(
    graph,
    incident_lat,
    incident_lon,
    facilities,
):
    """
    Rank emergency facilities by estimated travel time
    from the incident location.
    """

    ranked = []

    for facility in facilities:

        try:

            result = route_from_coordinates(
                graph,
                incident_lat,
                incident_lon,
                facility.latitude,
                facility.longitude,
            )

            ranked.append(
                {
                    "facility_id": facility.facility_id,
                    "name": facility.name,
                    "facility_type": facility.facility_type,
                    "latitude": facility.latitude,
                    "longitude": facility.longitude,
                    "distance_m": result["distance_m"],
                    "travel_time_s": result["travel_time_s"],
                    "route": result["route"],
                }
            )

        except Exception:

            continue

    ranked.sort(
        key=lambda item: item["travel_time_s"]
    )

    return ranked


def recommend_facility(
    graph,
    incident_lat,
    incident_lon,
    facilities,
):
    """
    Return the fastest reachable emergency facility.
    """

    ranked = rank_facilities(
        graph,
        incident_lat,
        incident_lon,
        facilities,
    )

    if not ranked:
        return None

    return ranked[0]