import osmnx as ox

from backend.services.graph_builder import prepare_graph
from backend.services.routing import (
    find_fastest_route,
    route_distance,
)


GRAPH_PATH = "data/raw/osm/adyar_drive.graphml"


graph = ox.load_graphml(GRAPH_PATH)

graph = prepare_graph(graph)

nodes = list(graph.nodes)

origin = nodes[0]
destination = nodes[-1]

route, travel_time = find_fastest_route(
    graph,
    origin,
    destination,
)

distance = route_distance(graph, route)

print("\n=== CIVORA ROUTING TEST ===")
print(f"Origin: {origin}")
print(f"Destination: {destination}")
print(f"Nodes in route: {len(route)}")
print(f"Distance: {distance:.2f} m")
print(f"Travel time: {travel_time:.2f} s")