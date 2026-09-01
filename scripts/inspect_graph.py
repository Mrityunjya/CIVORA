import osmnx as ox

GRAPH_PATH = "data/raw/osm/adyar_drive.graphml"

graph = ox.load_graphml(GRAPH_PATH)

print("\n=== CIVORA URBAN GRAPH ===")
print(f"Nodes: {len(graph.nodes)}")
print(f"Edges: {len(graph.edges)}")

print("\nSample node:")
node_id = list(graph.nodes)[0]
print(graph.nodes[node_id])

print("\nSample edge:")
edge = list(graph.edges(data=True))[0]
print(edge)