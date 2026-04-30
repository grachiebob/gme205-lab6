from math import sqrt

class SpatialObject:
    def __init__(self, geometry):
        self.geometry = geometry

    def distance_to(self, other):
        x1, y1 = self.geometry
        x2, y2 = other.geometry
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def intersects(self, other, threshold=0.0):
        return self.distance_to(other) <= threshold
    
    def __str__(self):
        return f"{self.__class__.__name__}(geometry={self.geometry})"