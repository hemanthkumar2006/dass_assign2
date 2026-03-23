import pytest
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import create_property

def test_find_winner_returns_highest_net_worth():
    game = Game(["Alice", "Bob"])
    alice = game.players[0]
    bob = game.players[1]
    
    alice.balance = 500
    bob.balance = 1000
    
    # max net worth is Bob's
    winner = game.find_winner()
    assert winner == bob

def test_trade_adds_money_to_seller():
    game = Game(["Alice", "Bob"])
    seller = game.players[0]
    buyer = game.players[1]
    
    seller.balance = 500
    buyer.balance = 1000
    
    prop = create_property("TestProp", 1, 200, 20)
    seller.add_property(prop)
    prop.owner = seller
    
    success = game.trade(seller, buyer, prop, 300)
    
    assert success is True
    assert buyer.balance == 700
    assert seller.balance == 800
    assert prop.owner == buyer
