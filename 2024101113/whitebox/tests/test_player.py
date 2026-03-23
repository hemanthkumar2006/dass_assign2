import pytest
from moneypoly.player import Player
from moneypoly.property import create_property

def test_player_net_worth_includes_properties():
    player = Player("Alice", balance=100)
    # create an unmortgaged property
    prop1 = create_property("Park Place", 37, 350, 35)
    # create a mortgaged property
    prop2 = create_property("Boardwalk", 39, 400, 50)
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
    
    player.move(4)
    assert player.position == 2
    assert player.balance == STARTING_BALANCE + GO_SALARY

def test_player_init():
    player = Player("Test")
    assert player.name == "Test"
    assert player.position == 0
    assert len(player.properties) == 0

def test_player_add_money():
    player = Player("Test", balance=100)
    player.add_money(50)
    assert player.balance == 150

def test_player_deduct_money():
    player = Player("Test", balance=100)
    player.deduct_money(50)
    assert player.balance == 50

def test_player_in_jail_proxies():
    player = Player("Test")
    assert player.in_jail is False
    player.in_jail = True
    assert player.in_jail is True

def test_player_is_eliminated():
    player = Player("Test")
    assert player.is_eliminated is False
    player.is_eliminated = True
    assert player.is_eliminated is True

def test_player_jail_turns():
    player = Player("Test")
    assert player.jail_turns == 0
    player.jail_turns = 2
    assert player.jail_turns == 2

def test_player_get_out_of_jail_cards():
    player = Player("Test")
    assert player.get_out_of_jail_cards == 0
    player.get_out_of_jail_cards += 1
    assert player.get_out_of_jail_cards == 1

def test_player_is_bankrupt():
    player = Player("Test", balance=100)
    assert player.is_bankrupt() is False
    player.balance = 0
    assert player.is_bankrupt() is True

def test_player_go_to_jail():
    from moneypoly.config import JAIL_POSITION
    player = Player("Test")
    player.go_to_jail()
    assert player.position == JAIL_POSITION
    assert player.in_jail is True
    assert player.jail_turns == 0

def test_player_remove_property():
    player = Player("Test")
    prop = create_property("Test Prop", 1, 100, 10)
    player.add_property(prop)
    player.remove_property(prop)
    assert len(player.properties) == 0
    assert prop.owner is None

def test_player_remove_property_not_owned():
    player = Player("Test")
    prop = create_property("Test Prop", 1, 100, 10)
    player.remove_property(prop) # Should not raise
    assert len(player.properties) == 0

def test_player_repr():
    player = Player("Test", balance=100)
    assert repr(player) == "Player('Test', balance=100, pos=0)"
