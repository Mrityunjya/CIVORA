import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two geographic points in meters."""

    earth_radius = 6_371_000

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    return 2 * earth_radius * math.asin(math.sqrt(a))


def identify_affected_edges(
    graph,
    incident_lat,
    incident_lon,
    radius_m=100,
):
    """
    Identify road segments whose endpoints fall
    within the incident radius.
    """

    affected_edges = []

    for u, v, key, data in graph.edges(
        keys=True,
        data=True,
    ):

        u_lat = float(graph.nodes[u]["y"])
        u_lon = float(graph.nodes[u]["x"])

        v_lat = float(graph.nodes[v]["y"])
        v_lon = float(graph.nodes[v]["x"])

        distance_u = haversine_distance(
            incident_lat,
            incident_lon,
            u_lat,
            u_lon,
        )

        distance_v = haversine_distance(
            incident_lat,
            incident_lon,
            v_lat,
            v_lon,
        )

        if min(distance_u, distance_v) <= radius_m:
            affected_edges.append((u, v, key))

    return affected_edges


def close_road_segments(graph, affected_edges):
    """Return a copy of the graph with affected roads removed."""

    modified_graph = graph.copy()

    for u, v, key in affected_edges:

        if modified_graph.has_edge(u, v, key):
            modified_graph.remove_edge(u, v, key)

    return modified_graph


def apply_incident(
    graph,
    incident_lat,
    incident_lon,
    radius_m=100,
):
    """Apply a geographic incident to the urban network."""

    affected_edges = identify_affected_edges(
        graph,
        incident_lat,
        incident_lon,
        radius_m,
    )

    modified_graph = close_road_segments(
        graph,
        affected_edges,
    )

    return modified_graph, affected_edges