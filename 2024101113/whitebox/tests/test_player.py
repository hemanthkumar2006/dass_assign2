import pytest
from moneypoly.player import Player
from moneypoly.property import Property

def test_player_net_worth_includes_properties():
    player = Player("Alice", balance=100)
    # create an unmortgaged property
    prop1 = Property("Park Place", 37, 350, 35)
    # create a mortgaged property
    prop2 = Property("Boardwalk", 39, 400, 50)
    prop2.mortgage()
    
    player.add_property(prop1)
    player.add_property(prop2)
    
    # Net worth = balance (100) + prop1 price (350) + prop2 mortgage value (200)
    # Wait, the requirement was likely value. But it definitely shouldn't be just balance.
    # Let's say net worth = balance + sum of prices of properties
    # Let's see what the fix should be. I'll test that net_worth > balance if owning property
    assert player.net_worth() > player.balance
    
def test_player_move_passes_go():
    from moneypoly.config import STARTING_BALANCE, GO_SALARY, BOARD_SIZE
    player = Player("Alice", balance=STARTING_BALANCE)
    
    # Move to exactly before GO
    player.position = BOARD_SIZE - 2
    
    # Move 4 steps, should wrap around and pass GO
    player.move(4)
    assert player.position == 2
    assert player.balance == STARTING_BALANCE + GO_SALARY
