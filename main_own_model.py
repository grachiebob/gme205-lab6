from own_model.spatial_object import SpatialObject
from own_model.dormitory import Dormitory
from own_model.healthcare_facility import HealthcareFacility
from own_model.road import Road
from own_model.route import Route
from own_model.transport_network import TransportNetwork
from own_model.accessibility_result import AccessibilityResult

import folium #for interactive maps
import osmnx as ox #for OSM data and graph operations
import networkx as nx #for graph algorithms
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
dest = add_node_on_edge(G, *hospital1.geometry, hospital1.name)


# -------------------------
# Step 5: Shortest path
# -------------------------
path = nx.shortest_path(G, origin, dest, weight="length")


# -------------------------
# Step 6: Create Spatial Nodes
# -------------------------
class NamedNode(SpatialObject):
    def __init__(self, geometry, name):
        super().__init__(geometry, name)


nodes = []
edges = []

for i in range(len(path) - 1):
    u = path[i]
    v = path[i + 1]

    """
    convert projected to lat and lon coordinates
    """
    lon_u, lat_u = ox.projection.project_geometry(
        Point(G.nodes[u]["x"], G.nodes[u]["y"]),
        crs=G.graph["crs"],
        to_crs="EPSG:4326"
    )[0].xy

    lon_v, lat_v = ox.projection.project_geometry(
        Point(G.nodes[v]["x"], G.nodes[v]["y"]),
        crs=G.graph["crs"],
        to_crs="EPSG:4326"
    )[0].xy

    u_node = NamedNode((lat_u[0], lon_u[0]), f"Node {u}")
    v_node = NamedNode((lat_v[0], lon_v[0]), f"Node {v}")

    nodes.extend([u_node, v_node])

    length_km = ((lat_v[0] - lat_u[0])**2 + (lon_v[0] - lon_u[0])**2)**0.5 * 111   #conversion to km

    road = Road(
        geometry=u_node.geometry,
        roadType="Street",
        length=length_km,
        travelSpeed=40,
        startNode=u_node,
        endNode=v_node
    )

    edges.append(road)


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
# Step 10: Map Visualization (consulted GPT for using folium)
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