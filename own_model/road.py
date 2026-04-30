from own_model.spatial_object import SpatialObject

class Road(SpatialObject):
    def __init__(self, geometry, roadType, length, travelSpeed, startNode, endNode):
        super().__init__(geometry)
        self.roadType = roadType
        self.length = length            # km
        self.travelSpeed = travelSpeed  # km/h
        self.startNode = startNode
        self.endNode = endNode

    def getLength(self):
        return self.length

    def getTravelTime(self):
        """
        Get the travel time on the road in hours.
        """
        t = self.length / self.travelSpeed
        """
        minimum 30 seconds (~0.0083 h) to avoid too small numbers (consulted GPT for this threshold)
        """
        return max(t, 0.0083)