from models.spatial_object import SpatialObject
from models.parcel import Parcel
from models.building import Building
from models.road import Road
from models.household import Household

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def main():
    # ---------------------------------------------------------
    # 1. Create parcels
    # ---------------------------------------------------------

    p1 = Parcel(geometry=(15, 20), parcel_id="p101", area=650.0, zone="Residential")
    p2 = Parcel(geometry=(50, 25), parcel_id="p102", area=1200.0, zone="Commercial")
    p3 = Parcel(geometry=(30, 45), parcel_id="p103", area=900.0, zone="Industrial")

    # ---------------------------------------------------------
    # 2. Create buildings and assign them to parcels
    # ---------------------------------------------------------

    b1 = Building(geometry=(16, 21), building_id="b101", height=15.5, usage="Residential", parcel=p1)
    b2 = Building(geometry=(51, 26), building_id="b102", height=30.0, usage="Office", parcel=p2)
    b3 = Building(geometry=(31, 46), building_id="b103", height=25.0, usage="Warehouse", parcel=p3)

    # ---------------------------------------------------------
    # 3. Create road and connect it to parcels
    # ---------------------------------------------------------

    r1= Road(geometry=(45, 40), road_id="r1", length=200.0, road_type="Primary")
    r2 = Road(geometry=(20, 30), road_id="r2", length=150.0, road_type="Secondary")
    
    r1.add_adjacent_parcel(p1)
    r1.add_adjacent_parcel(p2)
    r1.add_adjacent_parcel(p3)
    r2.add_adjacent_parcel(p1)
    r2.add_adjacent_parcel(p2)
    r2.add_adjacent_parcel(p3)

    # ---------------------------------------------------------
    # 4. Create households and assign them to buildings
    # ---------------------------------------------------------

    hh1 = Household(household_id="hh1", num_people=4, income=35000.0, tenure_type="Owner", building=b1)
    hh2 = Household(household_id="hh2", num_people=2, income=22000.0, tenure_type="Renter", building=b2)
    hh3 = Household(household_id="hh3", num_people=5, income=45000.0, tenure_type="Owner", building=b3)
    hh4 = Household(household_id="hh4", num_people=3, income=30000.0, tenure_type="Renter", building=b1)

    # ---------------------------------------------------------
    # 5. Show object descriptions
    # ---------------------------------------------------------

    print_header("PARCELS")
    print(p1.describe())
    print(p2.describe())
    print(p3.describe())

    print_header("BUILDINGS")
    print(b1.describe())
    print(b2.describe())
    print(b3.describe())

    print_header("ROADS")
    print(r1.describe())
    print(r2.describe())

    print_header("HOUSEHOLDS")
    print(hh1.describe())
    print(hh2.describe())
    print(hh3.describe())
    print(hh4.describe())

    # ---------------------------------------------------------
    # 6. Demonstrate class-specific behaviors
    # ---------------------------------------------------------

    print_header("CLASS-SPECIFIC METHODS")
    print(f"{p1.parcel_id} area: {p1.compute_area()} sqm")
    print(f"{p2.parcel_id} area: {p2.compute_area()} sqm")
    print(f"{b1.building_id} height: {b1.get_height()} m")
    print(f"{b2.building_id} height: {b2.get_height()} m")
    print(f"{r1.road_id} length: {r1.get_length()} m")
    print(f"{r2.road_id} length: {r2.get_length()} m")
    print(f"{hh1.household_id} total income: ₱{hh1.calculate_total_income()}")
    print(f"{hh3.household_id} total income: ₱{hh3.calculate_total_income()}")
    print(f"{b1.building_id} combined household income: ₱{b1.total_household_income()}")
    print(f"{b3.building_id} combined household income: ₱{b3.total_household_income()}")

    # ---------------------------------------------------------
    # 7. Demonstrate shared spatial behavior
    # ---------------------------------------------------------

    print_header("SHARED SPATIAL BEHAVIOR")
    print(f"Distance from {p1.parcel_id} to {p2.parcel_id}: {p1.distance_to(p2):.2f} units")
    print(f"Distance from {p1.parcel_id} to {p3.parcel_id}: {p1.distance_to(p3):.2f} units")
    print(f"Distance from {b1.building_id} to {r1.road_id}: {b1.distance_to(r1):.2f} units")
    print(f"Distance from {b2.building_id} to {r2.road_id}: {b2.distance_to(r2):.2f} units")
    print(f"Does {p1.parcel_id} intersect {b1.building_id}? {p1.intersects(b1)}")
    print(f"Does {p2.parcel_id} intersect {p3.parcel_id}? {p2.intersects(p3)}")

    # ---------------------------------------------------------
    # 8. Demonstrate relationships explicitly
    # ---------------------------------------------------------

    print_header("RELATIONSHIPS")
    print(f"Building {b1.building_id} is located on Parcel {b1.parcel.parcel_id}")
    print(f"Building {b2.building_id} is located on Parcel {b2.parcel.parcel_id}")
    print(f"Building {b3.building_id} is located on Parcel {b3.parcel.parcel_id}")

    print(f"\nHouseholds in Building {b1.building_id}:")
    for household in b1.households:
        print(f"  - Household {household.household_id} ({household.num_people} people)")

    print(f"\nHouseholds in Building {b3.building_id}:")
    for household in b3.households:
        print(f"  - Household {household.household_id} ({household.num_people} people)")

    print(f"\nRoad {r1.road_id} connections:")
    for parcel in r1.adjacent_parcels:
        print(f"  - Adjacent to Parcel {parcel.parcel_id}")

    print(f"\nRoad {r2.road_id} connections:")
    for parcel in r2.adjacent_parcels:
        print(f"  - Adjacent to Parcel {parcel.parcel_id}")

    # ---------------------------------------------------------
    # 9. Simple analysis examples
    # ---------------------------------------------------------

    print_header("SIMPLE ANALYSIS")
    print(f"Total households in {b1.building_id}: {len(b1.households)}")
    print(f"Total households in {b2.building_id}: {len(b2.households)}")
    print(f"Total households in {b3.building_id}: {len(b3.households)}")

    buildings_with_households = [b for b in [b1, b2, b3] if len(b.households) > 0]
    richer_building = max(buildings_with_households, key=lambda b: b.total_household_income())
    print(
        f"\nBuilding with highest total household income: "
        f"{richer_building.building_id} (₱{richer_building.total_household_income():.2f})"
    )

    total_people = sum(h.num_people for h in [hh1, hh2, hh3, hh4])
    print(f"\nTotal people across all households: {total_people}")

    avg_income = sum(h.income for h in [hh1, hh2, hh3, hh4]) / len([hh1, hh2, hh3, hh4])
    print(f"Average household income: ₱{avg_income:.2f}")


if __name__ == "__main__":
    main()