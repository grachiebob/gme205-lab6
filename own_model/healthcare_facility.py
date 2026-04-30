from own_model.spatial_object import SpatialObject

class HealthcareFacility(SpatialObject):
    def __init__(self, geometry, facilityID, name, facilityType):
        super().__init__(geometry, name)
        self.facilityID = facilityID
        self.facilityType = facilityType

    def getFacilityType(self):
        return self.facilityType