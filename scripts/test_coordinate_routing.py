import osmnx as ox

from backend.services.graph_builder import prepare_graph
from backend.services.routing import route_from_coordinates


GRAPH_PATH = "data/raw/osm/adyar_drive.graphml"


graph = ox.load_graphml(GRAPH_PATH)

graph = prepare_graph(graph)


# Example coordinates in Adyar
origin_lat = 13.0067
origin_lon = 80.2570

destination_lat = 13.0125
destination_lon = 80.2600


result = route_from_coordinates(
    graph,
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon,
)


print("\n=== CIVORA COORDINATE ROUTING ===")

print(f"Origin node: {result['origin_node']}")
print(f"Destination node: {result['destination_node']}")

print(f"Route nodes: {len(result['route'])}")

print(
    f"Distance: "
    f"{result['distance_m']:.2f} m"
)

print(
    f"Travel time: "
    f"{result['travel_time_s']:.2f} s"
)