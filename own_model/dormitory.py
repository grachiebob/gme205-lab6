from own_model.spatial_object import SpatialObject

class Dormitory(SpatialObject):
    def __init__(self, geometry, dormID, name):
        super().__init__(geometry, name)
        self.dormID = dormID

    def findNearestFacility(self, facilities, network):
        """
        Find the nearest healthcare facility to the dormitory.
        """
        nearest = min(facilities, key=lambda f: network.get_distance(self, f))
        return nearest