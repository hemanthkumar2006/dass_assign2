import pytest
from moneypoly.property import PropertyConfig, Property, create_property, PropertyGroup
from moneypoly.player import Player

def test_property_config_init():
    cfg = PropertyConfig(name="Vine", position=1, price=100, base_rent=10)
    assert getattr(cfg, "name") == "Vine"
    assert getattr(cfg, "price") == 100

def test_create_property():
    prop = create_property("Test", 5, 200, 20)
    assert prop.name == "Test"
    assert prop.position == 5
    assert prop.price == 200
    assert prop.base_rent == 20
    assert prop.mortgage_value == 100
    assert prop.owner is None
    assert prop.is_mortgaged is False

def test_property_get_rent():
    prop = create_property("Test", 5, 200, 20)
    assert prop.get_rent() == 20

def test_property_get_rent_group():
    group = PropertyGroup("Test Group", "blue")
    prop1 = create_property("Test1", 5, 200, 20, group)
    prop2 = create_property("Test2", 6, 200, 20, group)
    player = Player("Alice")
    prop1.owner = player
    prop2.owner = player
    
    assert group.all_owned_by(player) is True
    # Rent doubles
    assert prop1.get_rent() == 40

def test_property_get_rent_mortgaged():
    prop = create_property("Test", 5, 200, 20)
    prop.mortgage()
    assert prop.get_rent() == 0

def test_property_mortgage():
    prop = create_property("Test", 5, 200, 20)
    assert prop.mortgage() == 100
    assert prop.is_mortgaged is True
    assert prop.mortgage() == 0

def test_property_unmortgage():
    prop = create_property("Test", 5, 200, 20)
    # Not mortgaged
    assert prop.unmortgage() == 0 
    prop.mortgage()
    cost = prop.unmortgage()
    assert cost == 110 # 100 * 1.1
    assert prop.is_mortgaged is False

def test_property_is_available():
    prop = create_property("Test", 5, 200, 20)
    assert prop.is_available() is True
    prop.owner = Player("Alice")
    assert prop.is_available() is False
    prop.owner = None
    prop.mortgage()
    assert prop.is_available() is False

def test_property_repr():
    prop = create_property("Test", 5, 200, 20)
    assert repr(prop) == "Property('Test', pos=5, owner='unowned')"
    player = Player("Alice")
    prop.owner = player
    assert repr(prop) == "Property('Test', pos=5, owner='Alice')"

def test_propertygroup_init():
    group = PropertyGroup("Red", "red")
    assert group.name == "Red"
    assert group.size() == 0

def test_propertygroup_add_already_exists():
    group = PropertyGroup("Red", "red")
    prop = create_property("Test1", 5, 200, 20, group)
    assert group.size() == 1
    # Try re-adding
    group.add_property(prop)
    assert group.size() == 1

def test_propertygroup_all_owned_by_none():
    group = PropertyGroup("Red", "red")
    create_property("Test1", 5, 200, 20, group)
    assert group.all_owned_by(None) is False

def test_propertygroup_get_owner_counts():
    group = PropertyGroup("Red", "red")
    prop1 = create_property("Test1", 5, 200, 20, group)
    prop2 = create_property("Test2", 6, 200, 20, group)
    player = Player("Alice")
    prop1.owner = player
    prop2.owner = player
    counts = group.get_owner_counts()
    assert counts[player] == 2

def test_propertygroup_repr():
    group = PropertyGroup("Red", "red")
    assert repr(group) == "PropertyGroup('Red', 0 properties)"
