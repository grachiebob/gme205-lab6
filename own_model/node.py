from shapely.geometry import Point
import osmnx as ox

from own_model.spatial_object import SpatialObject
from own_model.road import Road


class NamedNode(SpatialObject):
    """
    A simple spatial node with a name attribute. (Consulted GPT for this class)
    """
    def __init__(self, geometry, name):
        super().__init__(geometry, name)


def build_spatial_nodes(G, path):
    nodes = []
    edges = []

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

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

        length_km = ((lat_v[0] - lat_u[0])**2 + (lon_v[0] - lon_u[0])**2)**0.5 * 111

        road = Road(
            geometry=u_node.geometry,
            roadType="Street",
            length=length_km,
            travelSpeed=40,
            startNode=u_node,
            endNode=v_node
        )

        edges.append(road)

    return nodes, edges