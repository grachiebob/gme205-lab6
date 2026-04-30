class Household:
    
    def __init__(self, household_id, num_people, income, tenure_type, building=None):
        self.household_id = household_id
        self.num_people = num_people
        self.income = income
        self.tenure_type = tenure_type
        self.building = building

        if self.building is not None:
            self.building.add_household(self)

    def calculate_total_income(self):
        return self.income
    
    def assign_building(self, building):
        self.building = building
        building.add_household(self)

    def describe(self):
        building_text = self.building.building_id if self.building else "None"
        return (
            f"Household {self.household_id}: people={self.num_people}, "
            f"income={self.income}, tenure={self.tenure_type}, "
            f"building={building_text}"
        )