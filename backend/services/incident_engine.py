import networkx as nx

from backend.models.incident import Incident


def identify_affected_edges(graph, node):
    """
    Identify road segments directly connected to an incident node.
    """

    affected_edges = []

    for u, v, key in graph.edges(
        node,
        keys=True,
    ):
        affected_edges.append((u, v, key))

    return affected_edges


def close_road_segments(graph, affected_edges):
    """
    Create a modified graph with affected road segments removed.
    """

    modified_graph = graph.copy()

    for u, v, key in affected_edges:

        if modified_graph.has_edge(u, v, key):
            modified_graph.remove_edge(
                u,
                v,
                key,
            )

    return modified_graph


def apply_incident(graph, incident):
    """
    Apply an incident to the urban road network.
    """

    affected_edges = identify_affected_edges(
        graph,
        incident.node,
    )

    modified_graph = close_road_segments(
        graph,
        affected_edges,
    )

    return modified_graph, affected_edges