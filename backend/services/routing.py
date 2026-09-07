import networkx as nx


def find_fastest_route(graph, origin, destination):
    """
    Find the fastest route between two graph nodes
    using travel time as the edge weight.
    """

    route = nx.shortest_path(
        graph,
        origin,
        destination,
        weight="travel_time_s",
    )

    total_time = nx.shortest_path_length(
        graph,
        origin,
        destination,
        weight="travel_time_s",
    )

    return route, total_time


def route_distance(graph, route):
    """Calculate total route distance in meters."""

    distance = 0.0

    for u, v in zip(route[:-1], route[1:]):
        edge_data = graph.get_edge_data(u, v)

        # MultiDiGraph may contain multiple edges.
        edge = min(
            edge_data.values(),
            key=lambda data: data.get("travel_time_s", float("inf"))
        )

        distance += edge.get("distance_m", 0)

    return distance