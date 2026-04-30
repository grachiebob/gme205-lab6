from math import sqrt

class SpatialObject:
    """
    Base class for all spatial objects (Dormitory, HealthcareFacility, and Road)
    """
    def __init__(self, geometry, name=None):
        self.geometry = geometry
        self.name = name

    def __hash__(self):
        return hash((self.geometry, self.name))

    def __eq__(self, other):
        return (self.geometry, self.name) == (other.geometry, other.name)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def distance_to(self, other):
        if not isinstance(other, SpatialObject):
            raise TypeError("distance_to expects a SpatialObject")

        x1, y1 = self.geometry
        x2, y2 = other.geometry

        return sqrt((x2 - x1)**2 + (y2 - y1)**2)