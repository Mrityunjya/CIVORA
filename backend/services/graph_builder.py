import osmnx as ox


def load_urban_graph(path: str):
    """Load a saved OSM road graph."""
    graph = ox.load_graphml(path)
    return graph


def prepare_graph(graph):
    """Prepare road attributes required by CIVORA."""

    for u, v, key, data in graph.edges(keys=True, data=True):

        # Ensure distance exists
        length = float(data.get("length", 0))
        data["distance_m"] = length

        # OSM speed may be missing or represented as a list/string.
        speed = data.get("maxspeed")

        if isinstance(speed, list):
            speed = speed[0] if speed else None

        try:
            speed = float(str(speed).replace(" km/h", "").strip())
        except (TypeError, ValueError):
            speed = 30.0  # conservative default for V1

        data["speed_kmh"] = speed

        # Travel time in seconds
        if speed > 0:
            data["travel_time_s"] = (
                length / 1000
            ) / speed * 3600
        else:
            data["travel_time_s"] = float("inf")

        # Normalize road type
        highway = data.get("highway")

        if isinstance(highway, list):
            highway = highway[0] if highway else "unknown"

        data["road_type"] = highway or "unknown"

    return graph


if __name__ == "__main__":

    graph_path = "data/raw/osm/adyar_drive.graphml"

    print("Loading CIVORA urban graph...")

    graph = load_urban_graph(graph_path)

    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges)}")

    graph = prepare_graph(graph)

    print("\nGraph prepared successfully.")

    u, v, key, data = list(
        graph.edges(keys=True, data=True)
    )[0]

    print("\nSample CIVORA edge:")
    print(f"Distance: {data['distance_m']:.2f} m")
    print(f"Speed: {data['speed_kmh']:.2f} km/h")
    print(f"Travel time: {data['travel_time_s']:.2f} s")
    print(f"Road type: {data['road_type']}")