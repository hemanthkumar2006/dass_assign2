class BlackMarketModule:
    def __init__(self, inventory_module):
        self.inventory = inventory_module

    def buy_part(self, part_name, cost):
        if self.inventory.cash < cost:
            raise ValueError("Not enough cash to buy part.")
        self.inventory.update_cash(-cost)
        self.inventory.parts[part_name] = self.inventory.parts.get(part_name, 0) + 1
        return f"Bought {part_name} from black market."
