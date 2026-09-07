import networkx as nx
import osmnx as ox

from backend.services.graph_builder import prepare_graph
from backend.services.routing import route_from_coordinates
from backend.services.incident_engine import apply_incident


GRAPH_PATH = "data/raw/osm/adyar_drive.graphml"


# --------------------------------------------------
# Load graph
# --------------------------------------------------

graph = ox.load_graphml(GRAPH_PATH)

graph = prepare_graph(graph)


# --------------------------------------------------
# Define origin and destination
# --------------------------------------------------

origin_lat = 13.0067
origin_lon = 80.2570

destination_lat = 13.0125
destination_lon = 80.2600


# --------------------------------------------------
# NORMAL ROUTE
# --------------------------------------------------

normal_result = route_from_coordinates(
    graph,
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon,
)

print("\n=== NORMAL NETWORK ===")

print(
    f"Distance: "
    f"{normal_result['distance_m']:.2f} m"
)

print(
    f"Travel time: "
    f"{normal_result['travel_time_s']:.2f} s"
)


# --------------------------------------------------
# CREATE GEOGRAPHIC INCIDENT
# --------------------------------------------------

incident_node = normal_result["route"][
    len(normal_result["route"]) // 2
]

incident_lat = float(
    graph.nodes[incident_node]["y"]
)

incident_lon = float(
    graph.nodes[incident_node]["x"]
)

incident_radius = 100


print("\n=== INCIDENT ===")

print("Type: accident")
print("Severity: high")

print(
    f"Location: "
    f"{incident_lat:.6f}, "
    f"{incident_lon:.6f}"
)

print(
    f"Impact radius: "
    f"{incident_radius} m"
)


# --------------------------------------------------
# APPLY INCIDENT
# --------------------------------------------------

modified_graph, affected_edges = apply_incident(
    graph,
    incident_lat,
    incident_lon,
    radius_m=incident_radius,
)

print(
    f"Affected road segments: "
    f"{len(affected_edges)}"
)


# --------------------------------------------------
# REROUTE
# --------------------------------------------------

try:

    rerouted_result = route_from_coordinates(
        modified_graph,
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon,
    )

    print("\n=== AFTER INCIDENT ===")

    print(
        f"Distance: "
        f"{rerouted_result['distance_m']:.2f} m"
    )

    print(
        f"Travel time: "
        f"{rerouted_result['travel_time_s']:.2f} s"
    )


    # --------------------------------------------------
    # IMPACT ANALYSIS
    # --------------------------------------------------

    distance_change = (
        rerouted_result["distance_m"]
        - normal_result["distance_m"]
    )

    time_change = (
        rerouted_result["travel_time_s"]
        - normal_result["travel_time_s"]
    )


    print("\n=== INCIDENT IMPACT ===")

    print(
        f"Additional distance: "
        f"{distance_change:.2f} m"
    )

    print(
        f"Additional travel time: "
        f"{time_change:.2f} s"
    )


    if normal_result["travel_time_s"] > 0:

        delay_percentage = (
            time_change
            / normal_result["travel_time_s"]
        ) * 100

        print(
            f"Travel time increase: "
            f"{delay_percentage:.2f}%"
        )


except nx.NetworkXNoPath:

    print(
        "\nNo alternative route available."
    )