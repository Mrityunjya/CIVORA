import osmnx as ox


def identify_incident_road(
    graph,
    incident_lat,
    incident_lon,
):
    """
    Identify the road segment closest to the incident location.
    """

    u, v, key = ox.distance.nearest_edges(
        graph,
        X=incident_lon,
        Y=incident_lat,
    )

    return u, v, key


def close_incident_road(
    graph,
    incident_edge,
):
    """
    Close the road segment associated with the incident.

    For bidirectional roads, attempt to close the reverse
    direction as well.
    """

    modified_graph = graph.copy()

    u, v, key = incident_edge

    # Close the identified direction
    if modified_graph.has_edge(u, v, key):

        modified_graph.remove_edge(
            u,
            v,
            key,
        )

    # Close reverse direction when present
    reverse_edges = list(
        modified_graph.get_edge_data(
            v,
            u,
            default={},
        ).keys()
    )

    for reverse_key in reverse_edges:

        modified_graph.remove_edge(
            v,
            u,
            reverse_key,
        )

    return modified_graph


def apply_incident(
    graph,
    incident_lat,
    incident_lon,
):
    """
    Apply a geographic incident to the nearest road segment.

    Returns:
        modified_graph
        affected_edges
        incident_edge
    """

    incident_edge = identify_incident_road(
        graph,
        incident_lat,
        incident_lon,
    )

    modified_graph = close_incident_road(
        graph,
        incident_edge,
    )

    affected_edges = [
        incident_edge
    ]

    return (
        modified_graph,
        affected_edges,
        incident_edge,
    )