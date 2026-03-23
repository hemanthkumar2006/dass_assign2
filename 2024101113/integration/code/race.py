class RaceManagementModule:
    def __init__(self, crew_module, inventory_module):
        self.crew = crew_module
        self.inventory = inventory_module

    def create_race(self, driver_name, car_name):
        drivers = self.crew.get_members_by_role("driver")
        if driver_name not in drivers:
            raise ValueError(f"{driver_name} is not a valid driver for a race.")
        if car_name not in self.inventory.cars:
            raise ValueError(f"Car {car_name} not available in inventory.")
        if self.inventory.cars[car_name]["condition"] < 50:
            raise ValueError(f"{car_name} is too damaged to race.")
        return {"driver": driver_name, "car": car_name, "status": "Ready"}

