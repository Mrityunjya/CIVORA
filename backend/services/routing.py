import networkx as nx
import osmnx as ox


def find_nearest_node(graph, latitude, longitude):
    """Find the nearest road node to a geographic coordinate."""

    node = ox.distance.nearest_nodes(
        graph,
        X=longitude,
        Y=latitude,
    )

    return node


def find_fastest_route(graph, origin, destination):
    """Find the fastest route using travel time."""

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

        edge = min(
            edge_data.values(),
            key=lambda data: data.get(
                "travel_time_s",
                float("inf"),
            ),
        )

        distance += edge.get("distance_m", 0)

    return distance


def route_from_coordinates(
    graph,
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon,
):
    """Calculate fastest route directly from geographic coordinates."""

    origin_node = find_nearest_node(
        graph,
        origin_lat,
        origin_lon,
    )

    destination_node = find_nearest_node(
        graph,
        destination_lat,
        destination_lon,
    )

    route, travel_time = find_fastest_route(
        graph,
        origin_node,
        destination_node,
    )

    distance = route_distance(
        graph,
        route,
    )

    return {
        "origin_node": origin_node,
        "destination_node": destination_node,
        "route": route,
        "distance_m": distance,
        "travel_time_s": travel_time,
    }