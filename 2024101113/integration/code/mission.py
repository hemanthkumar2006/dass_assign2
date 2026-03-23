class MissionPlanningModule:
    def __init__(self, crew_module, inventory_module):
        self.crew = crew_module
        self.inventory = inventory_module

    def assign_mission(self, mission_name, required_role, car_name):
        if car_name not in self.inventory.cars:
            raise ValueError(f"{car_name} not available in inventory.")
        
        # If car condition is low, require a mechanic
        if self.inventory.cars[car_name]["condition"] < 50 and required_role != "mechanic":
            raise ValueError(f"Car {car_name} is damaged. Requires a mechanic.")

        members = self.crew.get_members_by_role(required_role)
        if not members:
            raise ValueError(f"No {required_role} available for mission {mission_name}.")
        return f"Mission {mission_name} started with {members[0]} and {car_name}."

