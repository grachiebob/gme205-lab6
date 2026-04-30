from models.spatial_object import SpatialObject

class Parcel(SpatialObject):
    def __init__(self, geometry, parcel_id, area, zone):
        super().__init__(geometry)
        self.parcel_id = parcel_id
        self.area = area
        self.zone = zone
        self.buildings = []
        self.adjacent_roads = []

    def compute_area(self):
        return self.area
    
    def add_building(self, building):
        if building not in self.buildings:
            self.buildings.append(building)

    def add_adjacent_road(self, road):
        if road not in self.adjacent_roads:
            self.adjacent_roads.append(road)

    def describe(self):
        return (
            f"Parcel {self.parcel_id}: zone={self.zone}, "
            f"area={self.area}, buildings={len(self.buildings)}, "
            f"adjacent_roads={len(self.adjacent_roads)}"
        )