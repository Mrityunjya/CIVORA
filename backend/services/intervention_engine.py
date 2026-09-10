from backend.services.evacuation_engine import (
    simulate_evacuation,
    compare_evacuation,
)


def evaluate_intervention(
    graph,
    normal_results,
    evacuation_origins,
    safe_zone_lat,
    safe_zone_lon,
    intervention_id,
    name,
    description,
):
    """
    Evaluate an intervention by comparing evacuation
    performance against the normal network.
    """

    incident_results = simulate_evacuation(
        graph,
        evacuation_origins,
        safe_zone_lat,
        safe_zone_lon,
    )

    comparison = compare_evacuation(
        normal_results,
        incident_results,
    )

    reachable = [
        result
        for result in comparison
        if result["reachable"]
    ]

    blocked = [
        result
        for result in comparison
        if not result["reachable"]
    ]

    affected_population = sum(
        result["population"]
        for result in blocked
    )

    total_additional_time = sum(
        result["additional_time_s"]
        for result in reachable
        if result["additional_time_s"] is not None
    )

    total_additional_distance = sum(
        result["additional_distance_m"]
        for result in reachable
        if result["additional_distance_m"] is not None
    )

    reachable_count = len(reachable)
    blocked_count = len(blocked)

    # --------------------------------------------------
    # INTERVENTION SCORE
    # --------------------------------------------------
    #
    # Higher score = better intervention.
    #
    # Reachability is heavily weighted.
    # Delay and distance are secondary penalties.
    #

    score = (
        reachable_count * 1000
        - blocked_count * 2000
        - affected_population * 0.5
        - total_additional_time * 0.1
        - total_additional_distance * 0.01
    )

    return {
        "intervention_id": intervention_id,
        "name": name,
        "description": description,
        "reachable_origins": reachable_count,
        "blocked_origins": blocked_count,
        "affected_population": affected_population,
        "total_additional_time_s": total_additional_time,
        "total_additional_distance_m": total_additional_distance,
        "score": score,
        "comparison": comparison,
    }


def rank_interventions(results):
    """
    Rank interventions from best to worst.
    """

    ranked = sorted(
        results,
        key=lambda result: result["score"],
        reverse=True,
    )

    for index, result in enumerate(
        ranked,
        start=1,
    ):
        result["rank"] = index
        result["recommended"] = index == 1

    return ranked


def recommend_intervention(results):
    """
    Return the highest-scoring intervention.
    """

    if not results:
        return None

    ranked = rank_interventions(results)

    return ranked[0]