from own_model.spatial_object import SpatialObject
from own_model.dormitory import Dormitory
from own_model.healthcare_facility import HealthcareFacility
from own_model.road import Road
from own_model.route import Route
from own_model.transport_network import TransportNetwork
from own_model.accessibility_result import AccessibilityResult
from own_model.node import build_spatial_nodes

import folium #for interactive maps
import osmnx as ox #for OSM data and graph operations
import networkx as nx #for graph algorithms
import json
from shapely.geometry import Point


# -------------------------
# Step 1: Create Objects
# -------------------------
dorm1 = Dormitory((14.6042, 120.9822), 1, "Dorm A")

hospital1 = HealthcareFacility((14.6095, 120.9842), 3, "Manila General Hospital", "Hospital")

clinic1 = HealthcareFacility((14.6028, 120.9810), 4, "Recto Health Center", "Clinic")

# -------------------------
# Step 2: Load OSM Network (consulted GPT in using OSM)
# -------------------------
G = ox.graph_from_address(
    "Recto Avenue, Manila, Philippines",
    dist=3000,
    network_type="drive"
)

G = ox.project_graph(G)


# -------------------------
# Step 3: Add custom nodes (consultated the GPt for other ways to create nodes)
# -------------------------
def add_node_on_edge(G, lat, lon, name):
    point = Point(lon, lat)
    point_proj = ox.projection.project_geometry(point, to_crs=G.graph["crs"])[0]
    x, y = point_proj.x, point_proj.y

    u, v, key = ox.distance.nearest_edges(G, x, y)

    new_node = max(G.nodes) + 1
    G.add_node(new_node, x=x, y=y, name=name)

    xu, yu = G.nodes[u]["x"], G.nodes[u]["y"]
    xv, yv = G.nodes[v]["x"], G.nodes[v]["y"]

    dist_u = ((x - xu)**2 + (y - yu)**2)**0.5
    dist_v = ((x - xv)**2 + (y - yv)**2)**0.5

    G.add_edge(new_node, u, length=dist_u)
    G.add_edge(u, new_node, length=dist_u)

    G.add_edge(new_node, v, length=dist_v)
    G.add_edge(v, new_node, length=dist_v)

    return new_node


# -------------------------
# Step 4: Add nodes
# -------------------------
origin = add_node_on_edge(G, *dorm1.geometry, dorm1.name)
dest = add_node_on_edge(G, *clinic1.geometry, clinic1.name)


# -------------------------
# Step 5: Shortest path
# -------------------------
path = nx.shortest_path(G, origin, dest, weight="length")


# -------------------------
# Step 6: Create Spatial Nodes
# -------------------------
nodes, edges = build_spatial_nodes(G, path)


# -------------------------
# Step 7: Build Network
# -------------------------
unique_nodes = {n.name: n for n in nodes}.values()

network = TransportNetwork(
    nodes=list(unique_nodes),
    edges=edges
)

network.buildGraph()


# -------------------------
# Step 8: Create Route
# -------------------------
route = Route(
    1,
    edges[0].startNode,
    edges[-1].endNode,
    network
)

# -------------------------
# Step 9: OUTPUT
# -------------------------
print("========== ROUTE ==========")
print(route.describeRoute())

access = AccessibilityResult(route.distance, route.travelTime)
level = access.classifyAccessibility()

print(f"Accessibility Level: {level}")
print("============================")


# -------------------------
# Step 10: Save JSON Summary
# -------------------------
summary = {
    "origin": {
        "name": dorm1.name,
        "coordinates": dorm1.geometry
    },
    "destination": {
        "name": clinic1.name,
        "coordinates": clinic1.geometry
    },
    "distance_km": round(route.distance, 2),
    "travel_time": round(route.travelTime, 2),
    "accessibility": level,
    "total_roads": len(route.path_roads),

    "roads": [
        {
            "start_node": road.startNode.name,
            "end_node": road.endNode.name,
            "length_km": round(road.length, 2),
            "speed_kph": road.travelSpeed
        }
        for road in route.path_roads
    ]
}

with open("route_summary.json", "w") as file:
    json.dump(summary, file, indent=4)

print("JSON saved as route_summary.json")


# -------------------------
# Step 11: Map Visualization (consulted GPT for using folium)
# -------------------------
m = folium.Map(location=dorm1.geometry, zoom_start=16)

folium.Marker(dorm1.geometry, popup="Dorm A", icon=folium.Icon(color="blue")).add_to(m)
folium.Marker(hospital1.geometry, popup="Hospital", icon=folium.Icon(color="red")).add_to(m)
folium.Marker(clinic1.geometry, popup="Clinic", icon=folium.Icon(color="green")).add_to(m)

for road in route.path_roads:
    folium.PolyLine(
        [road.startNode.geometry, road.endNode.geometry],
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(m)

m.save("network_map.html")
print("Map saved as network_map.html")