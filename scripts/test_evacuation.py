import osmnx as ox

from backend.services.graph_builder import prepare_graph
from backend.services.incident_engine import apply_incident
from backend.services.evacuation_engine import (
    simulate_evacuation,
    compare_evacuation,
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
# NORMAL EVACUATION
# --------------------------------------------------

normal_results = simulate_evacuation(
    graph,
    EVACUATION_ORIGINS,
    safe_zone_lat,
    safe_zone_lon,
)


# --------------------------------------------------
# CREATE INCIDENT
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
# INCIDENT EVACUATION
# --------------------------------------------------

incident_results = simulate_evacuation(
    modified_graph,
    EVACUATION_ORIGINS,
    safe_zone_lat,
    safe_zone_lon,
)


# --------------------------------------------------
# COMPARE
# --------------------------------------------------

comparison = compare_evacuation(
    normal_results,
    incident_results,
)


# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print("\n=== CIVORA EVACUATION SIMULATION ===")

print(
    f"Safe zone: "
    f"{safe_zone_lat:.6f}, "
    f"{safe_zone_lon:.6f}"
)


for result in comparison:

    print(
        f"\n{result['name']}"
    )

    print(
        f"Population: "
        f"{result['population']}"
    )

    if result["reachable"]:

        print(
            f"Normal evacuation time: "
            f"{result['normal_time_s']:.2f} s"
        )

        print(
            f"After incident: "
            f"{result['incident_time_s']:.2f} s"
        )

        print(
            f"Additional time: "
            f"{result['additional_time_s']:.2f} s"
        )

        print(
            f"Additional distance: "
            f"{result['additional_distance_m']:.2f} m"
        )

    else:

        print(
            "EVACUATION PATH: BLOCKED"
        )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

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


print("\n=== EVACUATION SUMMARY ===")

print(
    f"Total origins: "
    f"{len(comparison)}"
)

print(
    f"Reachable origins: "
    f"{len(reachable)}"
)

print(
    f"Blocked origins: "
    f"{len(blocked)}"
)


if reachable:

    worst = max(
        reachable,
        key=lambda result:
        result["additional_time_s"],
    )

    print(
        f"Worst affected zone: "
        f"{worst['name']}"
    )

    print(
        f"Additional evacuation time: "
        f"{worst['additional_time_s']:.2f} s"
    )