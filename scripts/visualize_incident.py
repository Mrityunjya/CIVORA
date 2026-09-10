import networkx as nx
import osmnx as ox
import folium

from backend.services.graph_builder import prepare_graph
from backend.services.routing import route_from_coordinates
from backend.services.incident_engine import apply_incident


GRAPH_PATH = "data/raw/osm/adyar_drive.graphml"
OUTPUT_PATH = "data/civora_incident_demo.html"


# --------------------------------------------------
# LOAD GRAPH
# --------------------------------------------------

graph = ox.load_graphml(GRAPH_PATH)
graph = prepare_graph(graph)


# --------------------------------------------------
# COORDINATES
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

normal_route = normal_result["route"]


# --------------------------------------------------
# INCIDENT LOCATION
# --------------------------------------------------

incident_node = normal_route[
    len(normal_route) // 2
]

incident_lat = float(
    graph.nodes[incident_node]["y"]
)

incident_lon = float(
    graph.nodes[incident_node]["x"]
)

# Visual impact zone only.
incident_radius = 50


# --------------------------------------------------
# APPLY INCIDENT
# --------------------------------------------------

modified_graph, affected_edges, incident_edge = apply_incident(
    graph,
    incident_lat,
    incident_lon,
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

    rerouted_route = rerouted_result["route"]
    reroute_available = True

except (
    nx.NetworkXNoPath,
    nx.NodeNotFound,
):

    print(
        "\nWARNING: No alternative route available."
    )

    rerouted_result = None
    rerouted_route = []
    reroute_available = False


# --------------------------------------------------
# CREATE MAP
# --------------------------------------------------

m = folium.Map(
    location=[
        incident_lat,
        incident_lon,
    ],
    zoom_start=15,
)


# --------------------------------------------------
# ORIGIN
# --------------------------------------------------

folium.Marker(
    [origin_lat, origin_lon],
    popup="Origin",
    icon=folium.Icon(
        color="green",
        icon="play",
    ),
).add_to(m)


# --------------------------------------------------
# DESTINATION
# --------------------------------------------------

folium.Marker(
    [destination_lat, destination_lon],
    popup="Destination",
    icon=folium.Icon(
        color="red",
        icon="flag",
    ),
).add_to(m)


# --------------------------------------------------
# INCIDENT
# --------------------------------------------------

folium.Marker(
    [incident_lat, incident_lon],
    popup=(
        "CIVORA INCIDENT<br>"
        "Type: Accident<br>"
        "Severity: High<br>"
        "Affected road segment"
    ),
    icon=folium.Icon(
        color="orange",
        icon="warning-sign",
    ),
).add_to(m)


# --------------------------------------------------
# INCIDENT IMPACT ZONE
# --------------------------------------------------

folium.Circle(
    location=[
        incident_lat,
        incident_lon,
    ],
    radius=incident_radius,
    popup="Approximate incident impact zone",
    fill=True,
).add_to(m)


# --------------------------------------------------
# AFFECTED ROAD
# --------------------------------------------------

for u, v, key in affected_edges:

    if (
        u not in graph.nodes
        or v not in graph.nodes
    ):
        continue

    u_lat = float(
        graph.nodes[u]["y"]
    )

    u_lon = float(
        graph.nodes[u]["x"]
    )

    v_lat = float(
        graph.nodes[v]["y"]
    )

    v_lon = float(
        graph.nodes[v]["x"]
    )

    folium.PolyLine(
        [
            [u_lat, u_lon],
            [v_lat, v_lon],
        ],
        weight=7,
        opacity=0.9,
        popup="Closed road segment",
    ).add_to(m)


# --------------------------------------------------
# NORMAL ROUTE
# --------------------------------------------------

normal_coordinates = [
    [
        float(graph.nodes[node]["y"]),
        float(graph.nodes[node]["x"]),
    ]
    for node in normal_route
    if node in graph.nodes
]

folium.PolyLine(
    normal_coordinates,
    weight=5,
    opacity=0.7,
    popup="Normal fastest route",
).add_to(m)


# --------------------------------------------------
# REROUTED ROUTE
# --------------------------------------------------

if reroute_available:

    rerouted_coordinates = [
        [
            float(
                modified_graph.nodes[node]["y"]
            ),
            float(
                modified_graph.nodes[node]["x"]
            ),
        ]
        for node in rerouted_route
        if node in modified_graph.nodes
    ]

    folium.PolyLine(
        rerouted_coordinates,
        weight=6,
        opacity=0.9,
        popup="CIVORA recommended reroute",
    ).add_to(m)


# --------------------------------------------------
# SAVE MAP
# --------------------------------------------------

m.save(OUTPUT_PATH)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\n=== CIVORA INCIDENT MAP ===")

print(
    f"Map saved to: {OUTPUT_PATH}"
)

print(
    f"Normal distance: "
    f"{normal_result['distance_m']:.2f} m"
)

print(
    f"Affected roads: "
    f"{len(affected_edges)}"
)

print(
    f"Incident road segment: "
    f"{incident_edge}"
)

if reroute_available:

    print(
        f"Rerouted distance: "
        f"{rerouted_result['distance_m']:.2f} m"
    )

    time_change = (
        rerouted_result["travel_time_s"]
        - normal_result["travel_time_s"]
    )

    print(
        f"Additional travel time: "
        f"{time_change:.2f} s"
    )

else:

    print(
        "Rerouted distance: N/A"
    )

    print(
        "Alternative route: NOT AVAILABLE"
    )


print(
    "\nOpen the generated HTML file "
    "in your browser."
)