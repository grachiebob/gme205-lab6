from models.spatial_object import SpatialObject

class Road(SpatialObject):
    def __init__(self, geometry, road_id, length, road_type):
        super().__init__(geometry)
        self.road_id = road_id
        self.length = length
        self.road_type = road_type
        self.adjacent_parcels = []  

    def get_length(self):
        return self.length

    def add_adjacent_parcel(self, parcel):
        if parcel not in self.adjacent_parcels:
            self.adjacent_parcels.append(parcel)
            parcel.add_adjacent_road(self)

    def describe(self):
        parcel_ids = [p.parcel_id for p in self.adjacent_parcels]
        return (
            f"Road {self.road_id}: type={self.road_type}, "
            f"length={self.length}, adjacent_parcels={parcel_ids}"
        )