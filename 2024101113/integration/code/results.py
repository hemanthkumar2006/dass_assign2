class ResultsModule:
    def __init__(self, inventory_module):
        self.inventory = inventory_module

    def complete_race(self, race, position, prize_money):
        if race["status"] != "Ready":
            raise ValueError("Race was not ready.")
        self.inventory.update_cash(prize_money)
        # Assuming position 1 is a win
        damage = 10 if position == 1 else 30
        self.inventory.cars[race["car"]]["condition"] -= damage
        race["status"] = "Completed"
        return f"Race completed. Position {position}. Earned {prize_money}. Car took {damage} damage."

