import osmnx as ox

PLACE = "Adyar, Chennai, India"
OUTPUT = "data/raw/osm/adyar_drive.graphml"

print(f"Downloading road network for: {PLACE}")

graph = ox.graph_from_place(
    PLACE,
    network_type="drive",
    simplify=True
)

print(f"Nodes: {len(graph.nodes)}")
print(f"Edges: {len(graph.edges)}")

ox.save_graphml(graph, OUTPUT)

print(f"Graph saved to: {OUTPUT}")