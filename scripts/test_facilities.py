import osmnx as ox

from backend.services.graph_builder import prepare_graph
from backend.services.facility_engine import (
    rank_facilities,
    recommend_facility,
)

from data.sample.facilities import FACILITIES


GRAPH_PATH = "data/raw/osm/adyar_drive.graphml"


# --------------------------------------------------
# LOAD GRAPH
# --------------------------------------------------

graph = ox.load_graphml(
    GRAPH_PATH
)

graph = prepare_graph(
    graph
)


# --------------------------------------------------
# INCIDENT LOCATION
# --------------------------------------------------

incident_lat = 13.008252
incident_lon = 80.258969


# --------------------------------------------------
# RANK FACILITIES
# --------------------------------------------------

ranked = rank_facilities(
    graph,
    incident_lat,
    incident_lon,
    FACILITIES,
)


print("\n=== CIVORA EMERGENCY FACILITIES ===")


for index, facility in enumerate(
    ranked,
    start=1,
):

    print(
        f"\n{index}. {facility['name']}"
    )

    print(
        f"Type: "
        f"{facility['facility_type']}"
    )

    print(
        f"Distance: "
        f"{facility['distance_m']:.2f} m"
    )

    print(
        f"Travel time: "
        f"{facility['travel_time_s']:.2f} s"
    )


# --------------------------------------------------
# RECOMMENDATION
# --------------------------------------------------

recommended = recommend_facility(
    graph,
    incident_lat,
    incident_lon,
    FACILITIES,
)


print("\n=== CIVORA RECOMMENDATION ===")


if recommended:

    print(
        f"Recommended facility: "
        f"{recommended['name']}"
    )

    print(
        f"Estimated response time: "
        f"{recommended['travel_time_s']:.2f} s"
    )

else:

    print(
        "No reachable emergency facility."
    )