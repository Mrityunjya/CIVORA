import networkx as nx
import osmnx as ox

from backend.services.graph_builder import prepare_graph
from backend.services.routing import route_from_coordinates
from backend.services.incident_engine import apply_incident
from backend.models.incident import Incident


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
# CREATE INCIDENT
# --------------------------------------------------

incident_node = normal_result["route"][
    len(normal_result["route"]) // 2
]


incident = Incident(
    incident_id="INC-001",
    incident_type="accident",
    node=incident_node,
    severity="high",
)


print("\n=== INCIDENT ===")

print(f"Type: {incident.incident_type}")
print(f"Severity: {incident.severity}")
print(f"Node: {incident.node}")


# --------------------------------------------------
# APPLY INCIDENT
# --------------------------------------------------

modified_graph, affected_edges = apply_incident(
    graph,
    incident,
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
    # IMPACT
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

except nx.NetworkXNoPath:

    print("\nNo alternative route available.")