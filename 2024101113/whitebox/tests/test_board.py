import pytest
from moneypoly.board import Board, SPECIAL_TILES
from moneypoly.player import Player

def test_board_init():
    board = Board()
    assert len(board.groups) == 8
    assert len(board.properties) == 22

def test_get_property_at_exists():
    board = Board()
    prop = board.get_property_at(1)  # Mediterranean Ave
    assert prop is not None
    assert prop.name == "Mediterranean Avenue"

def test_get_property_at_none():
    board = Board()
    assert board.get_property_at(0) is None  # GO

def test_get_tile_type_special():
    board = Board()
    assert board.get_tile_type(0) == "go"
    assert board.get_tile_type(30) == "go_to_jail"

def test_get_tile_type_property():
    board = Board()
    assert board.get_tile_type(1) == "property"

def test_get_tile_type_blank():
    board = Board()
    assert board.get_tile_type(99) == "blank"

def test_is_purchasable_true():
    board = Board()
    assert board.is_purchasable(1) is True

def test_is_purchasable_false_not_property():
    board = Board()
    assert board.is_purchasable(0) is False

def test_is_purchasable_false_mortgaged():
    board = Board()
    prop = board.get_property_at(1)
    prop.mortgage()
    assert board.is_purchasable(1) is False

def test_is_purchasable_false_owned():
    board = Board()
    prop = board.get_property_at(1)
    player = Player("Alice")
    prop.owner = player
    assert board.is_purchasable(1) is False

def test_is_special_tile():
    board = Board()
    assert board.is_special_tile(0) is True
    assert board.is_special_tile(1) is False

def test_properties_owned_by():
    board = Board()
    player = Player("Alice")
    prop = board.get_property_at(1)
    prop.owner = player
    owned = board.properties_owned_by(player)
    assert len(owned) == 1
    assert owned[0] == prop

def test_unowned_properties():
    board = Board()
    unowned = board.unowned_properties()
    assert len(unowned) == 22

def test_board_repr():
    board = Board()
    assert repr(board) == "Board(22 properties, 0 owned)"
