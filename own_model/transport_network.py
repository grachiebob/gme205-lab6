import networkx as nx

class TransportNetwork:
    """
    Represents a transportation network with nodes and edges (roads). (Consulted GPT for the implementation of networkx)
    """
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges
        self.graph = nx.DiGraph()

    def buildGraph(self):
        for node in self.nodes:
            self.graph.add_node(node)
        for road in self.edges:
            self.graph.add_edge(road.startNode, road.endNode, weight=road.getTravelTime(), road=road)

    def find_shortest_path(self, origin, destination):
        return nx.shortest_path(self.graph, origin, destination, weight='weight')

    def get_distance(self, origin, destination):
        path = self.find_shortest_path(origin, destination)
        total_distance = 0
        for i in range(len(path)-1):
            edge_data = self.graph.get_edge_data(path[i], path[i+1])
            total_distance += edge_data['road'].getLength()
        return total_distance

    def get_travel_time(self, origin, destination):
        path = self.find_shortest_path(origin, destination)
        total_time = 0
        for i in range(len(path)-1):
            edge_data = self.graph.get_edge_data(path[i], path[i+1])
            total_time += edge_data['road'].getTravelTime()
        return total_time

    def get_path_roads(self, origin, destination):
        path_nodes = self.find_shortest_path(origin, destination)
        roads = []
        for i in range(len(path_nodes)-1):
            edge_data = self.graph.get_edge_data(path_nodes[i], path_nodes[i+1])
            roads.append(edge_data['road'])
        return roads