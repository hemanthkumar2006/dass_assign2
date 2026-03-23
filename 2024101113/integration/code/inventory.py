class InventoryModule:
    def __init__(self, cash=0):
        self.cash = cash
        self.cars = {}
        self.parts = {}

    def add_car(self, name, condition=100):
        self.cars[name] = {"condition": condition}

    def update_cash(self, amount):
        self.cash += amount

    def get_car_condition(self, name):
        return self.cars.get(name, {}).get("condition", 0)

