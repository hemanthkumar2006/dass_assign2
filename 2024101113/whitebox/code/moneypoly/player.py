"""Module containing the Player class for the MoneyPoly game."""
from dataclasses import dataclass
from moneypoly.config import STARTING_BALANCE, BOARD_SIZE, GO_SALARY, JAIL_POSITION


@dataclass
class JailState:
    """Groups all jail-related state for a player into one object."""

    in_jail: bool = False
    jail_turns: int = 0
    get_out_of_jail_cards: int = 0
    is_eliminated: bool = False


class Player:
    """Represents a single player in a MoneyPoly game."""

    def __init__(self, name, balance=STARTING_BALANCE):
        self.name = name
        self.balance = balance
        self.position = 0
        self.properties = []
        self._jail = JailState()


    def add_money(self, amount):
        """Add funds to this player's balance. Amount must be non-negative."""
        if amount < 0:
            raise ValueError(f"Cannot add a negative amount: {amount}")
        self.balance += amount

    def deduct_money(self, amount):
        """Deduct funds from this player's balance. Amount must be non-negative."""
        if amount < 0:
            raise ValueError(f"Cannot deduct a negative amount: {amount}")
        self.balance -= amount

    # ------------------------------------------------------------------
    # Jail state proxies – keep the public API unchanged
    # ------------------------------------------------------------------

    @property
    def in_jail(self):
        """Return True if this player is currently in jail."""
        return self._jail.in_jail

    @in_jail.setter
    def in_jail(self, value):
        self._jail.in_jail = value

    @property
    def jail_turns(self):
        """Return the number of turns this player has been in jail."""
        return self._jail.jail_turns

    @jail_turns.setter
    def jail_turns(self, value):
        self._jail.jail_turns = value

    @property
    def get_out_of_jail_cards(self):
        """Return how many Get Out of Jail Free cards this player holds."""
        return self._jail.get_out_of_jail_cards

    @get_out_of_jail_cards.setter
    def get_out_of_jail_cards(self, value):
        self._jail.get_out_of_jail_cards = value

    @property
    def is_eliminated(self):
        """Return True if this player has been eliminated from the game."""
        return self._jail.is_eliminated

    @is_eliminated.setter
    def is_eliminated(self, value):
        self._jail.is_eliminated = value

    # ------------------------------------------------------------------

    def is_bankrupt(self):
        """Return True if this player has no money remaining."""
        return self.balance <= 0

    def net_worth(self):
        """Calculate and return this player's total net worth."""
        total = self.balance
        for prop in self.properties:
            if not prop.is_mortgaged:
                total += prop.price
            else:
                total += prop.mortgage_value
        return total

    def move(self, steps):
        """
        Move this player forward by `steps` squares, wrapping around the board.
        Awards the Go salary if the player passes or lands on Go.
        Returns the new board position.
        """
        old_position = self.position
        self.position = (self.position + steps) % BOARD_SIZE

        if old_position + steps >= BOARD_SIZE:
            self.add_money(GO_SALARY)
            print(f"  {self.name} landed on Go and collected ${GO_SALARY}.")

        return self.position

    def go_to_jail(self):
        """Send this player directly to the Jail square."""
        self.position = JAIL_POSITION
        self.in_jail = True
        self.jail_turns = 0


    def add_property(self, prop):
        """Add a property tile to this player's holdings."""
        if prop not in self.properties:
            self.properties.append(prop)

    def remove_property(self, prop):
        """Remove a property tile from this player's holdings."""
        if prop in self.properties:
            self.properties.remove(prop)

    def count_properties(self):
        """Return the number of properties this player currently owns."""
        return len(self.properties)


    def status_line(self):
        """Return a concise one-line status string for this player."""
        jail_tag = " [JAILED]" if self.in_jail else ""
        return (
            f"{self.name}: ${self.balance}  "
            f"pos={self.position}  "
            f"props={len(self.properties)}"
            f"{jail_tag}"
        )

    def __repr__(self):
        return f"Player({self.name!r}, balance={self.balance}, pos={self.position})"
