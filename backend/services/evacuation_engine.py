from backend.services.routing import route_from_coordinates


def simulate_evacuation(
    graph,
    evacuation_origins,
    safe_zone_lat,
    safe_zone_lon,
):
    """
    Simulate evacuation from multiple origins
    toward a common safe zone.
    """

    results = []

    for origin in evacuation_origins:

        try:

            route_result = route_from_coordinates(
                graph,
                origin.latitude,
                origin.longitude,
                safe_zone_lat,
                safe_zone_lon,
            )

            results.append(
                {
                    "origin_id": origin.origin_id,
                    "name": origin.name,
                    "population": origin.population,
                    "distance_m": route_result[
                        "distance_m"
                    ],
                    "travel_time_s": route_result[
                        "travel_time_s"
                    ],
                    "route": route_result["route"],
                    "reachable": True,
                }
            )

        except Exception:

            results.append(
                {
                    "origin_id": origin.origin_id,
                    "name": origin.name,
                    "population": origin.population,
                    "distance_m": None,
                    "travel_time_s": None,
                    "route": [],
                    "reachable": False,
                }
            )

    return results


def compare_evacuation(
    normal_results,
    incident_results,
):
    """
    Compare evacuation performance before and
    after an incident.
    """

    comparison = []

    normal_by_id = {
        result["origin_id"]: result
        for result in normal_results
    }

    for incident in incident_results:

        origin_id = incident["origin_id"]

        normal = normal_by_id.get(origin_id)

        if normal is None:

            continue

        if (
            normal["reachable"]
            and incident["reachable"]
        ):

            time_change = (
                incident["travel_time_s"]
                - normal["travel_time_s"]
            )

            distance_change = (
                incident["distance_m"]
                - normal["distance_m"]
            )

            comparison.append(
                {
                    "origin_id": origin_id,
                    "name": incident["name"],
                    "population": incident["population"],
                    "normal_time_s": normal[
                        "travel_time_s"
                    ],
                    "incident_time_s": incident[
                        "travel_time_s"
                    ],
                    "additional_time_s": time_change,
                    "additional_distance_m": distance_change,
                    "reachable": True,
                }
            )

        else:

            comparison.append(
                {
                    "origin_id": origin_id,
                    "name": incident["name"],
                    "population": incident["population"],
                    "normal_time_s": normal[
                        "travel_time_s"
                    ],
                    "incident_time_s": None,
                    "additional_time_s": None,
                    "additional_distance_m": None,
                    "reachable": False,
                }
            )

    return comparison