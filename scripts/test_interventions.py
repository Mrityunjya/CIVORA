import osmnx as ox

from backend.services.graph_builder import prepare_graph
from backend.services.incident_engine import apply_incident
from backend.services.evacuation_engine import (
    simulate_evacuation,
)

from backend.services.intervention_engine import (
    evaluate_intervention,
    rank_interventions,
    recommend_intervention,
)

from data.sample.evacuation_origins import (
    EVACUATION_ORIGINS,
)


GRAPH_PATH = "data/raw/osm/adyar_drive.graphml"


# --------------------------------------------------
# LOAD GRAPH
# --------------------------------------------------

graph = ox.load_graphml(
    GRAPH_PATH
)

graph = prepare_graph(
    graph
)


# --------------------------------------------------
# SAFE ZONE
# --------------------------------------------------

safe_zone_lat = 13.0045
safe_zone_lon = 80.2630


# --------------------------------------------------
# NORMAL NETWORK
# --------------------------------------------------

normal_results = simulate_evacuation(
    graph,
    EVACUATION_ORIGINS,
    safe_zone_lat,
    safe_zone_lon,
)


# --------------------------------------------------
# INCIDENT
# --------------------------------------------------

incident_lat = 13.008252
incident_lon = 80.258969

modified_graph, affected_edges, incident_edge = (
    apply_incident(
        graph,
        incident_lat,
        incident_lon,
    )
)


# --------------------------------------------------
# INTERVENTION 1
# --------------------------------------------------

incident_intervention = evaluate_intervention(
    modified_graph,
    normal_results,
    EVACUATION_ORIGINS,
    safe_zone_lat,
    safe_zone_lon,
    intervention_id="I001",
    name="Maintain Incident Closure",
    description=(
        "Keep the incident road closed "
        "and allow the network to reroute."
    ),
)


# --------------------------------------------------
# INTERVENTION 2
# --------------------------------------------------

# For V1, we use the same network as a second
# strategy placeholder. Later this will become
# a real road-opening / traffic-control action.

alternate_strategy = evaluate_intervention(
    modified_graph,
    normal_results,
    EVACUATION_ORIGINS,
    safe_zone_lat,
    safe_zone_lon,
    intervention_id="I002",
    name="Prioritize Evacuation Routing",
    description=(
        "Prioritize currently reachable "
        "evacuation corridors."
    ),
)


# --------------------------------------------------
# RANK
# --------------------------------------------------

results = rank_interventions(
    [
        incident_intervention,
        alternate_strategy,
    ]
)


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

print("\n=== CIVORA INTERVENTION ANALYSIS ===")

for result in results:

    print(
        f"\nRank {result['rank']}: "
        f"{result['name']}"
    )

    print(
        f"Description: "
        f"{result['description']}"
    )

    print(
        f"Reachable origins: "
        f"{result['reachable_origins']}"
    )

    print(
        f"Blocked origins: "
        f"{result['blocked_origins']}"
    )

    print(
        f"Affected population: "
        f"{result['affected_population']}"
    )

    print(
        f"Additional evacuation time: "
        f"{result['total_additional_time_s']:.2f} s"
    )

    print(
        f"Additional distance: "
        f"{result['total_additional_distance_m']:.2f} m"
    )

    print(
        f"Score: "
        f"{result['score']:.2f}"
    )


# --------------------------------------------------
# RECOMMENDATION
# --------------------------------------------------

recommended = recommend_intervention(
    results
)

print(
    "\n=== CIVORA RECOMMENDATION ==="
)

if recommended:

    print(
        f"Recommended intervention: "
        f"{recommended['name']}"
    )

    print(
        f"Reason: highest network "
        f"resilience score ({recommended['score']:.2f})"
    )

else:

    print(
        "No intervention available."
    )