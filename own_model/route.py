#Non-spatial object
class Route:
    def __init__(self, routeID, origin, destination, network):
        self.routeID = routeID
        self.origin = origin
        self.destination = destination
        self.network = network
        self.path_nodes = network.find_shortest_path(origin, destination)
        self.path_roads = network.get_path_roads(origin, destination)
        self.distance = network.get_distance(origin, destination)
        self.travelTime = network.get_travel_time(origin, destination)

    def calculateDistance(self):
        """
        Calculate the distance between origin and destination using the distance_to method.
        """
        return self.origin.distance_to(self.destination)

    def describeRoute(self):
        nodes_sequence = " -> ".join([node.name for node in self.path_nodes])
        roads_sequence = " | ".join([road.startNode.name + "->" + road.endNode.name for road in self.path_roads])
        return f"Route {self.routeID}:\nNodes: {nodes_sequence}\nRoads: {roads_sequence}\nDistance: {self.distance:.2f} km\nTravel Time: {self.travelTime:.2f} h"