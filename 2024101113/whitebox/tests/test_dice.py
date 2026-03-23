import pytest
from moneypoly.dice import Dice

def test_dice_init():
    dice = Dice()
    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0

def test_dice_reset():
    dice = Dice()
    dice.die1 = 5
    dice.die2 = 5
    dice.doubles_streak = 1
    dice.reset()
    assert dice.die1 == 0
    assert dice.die2 == 0
    assert dice.doubles_streak == 0

def test_dice_roll():
    dice = Dice()
    total = dice.roll()
    assert 2 <= total <= 10 # Since randint is 1 to 5 as per code
    assert 1 <= dice.die1 <= 5
    assert 1 <= dice.die2 <= 5

def test_dice_doubles_streak():
    dice = Dice()
    # Force doubles
    import random
    random.seed(42)  # May or may not hit doubles, but let's test logic directly
    dice.die1 = 3
    dice.die2 = 3
    assert dice.is_doubles() is True

def test_dice_total():
    dice = Dice()
    dice.die1 = 3
    dice.die2 = 4
    assert dice.total() == 7

def test_dice_describe():
    dice = Dice()
    dice.die1 = 2
    dice.die2 = 3
    assert dice.describe() == "2 + 3 = 5"
    dice.die1 = 4
    dice.die2 = 4
    assert dice.describe() == "4 + 4 = 8 (DOUBLES)"

def test_dice_repr():
    dice = Dice()
    dice.die1 = 1
    dice.die2 = 6
    assert repr(dice) == "Dice(die1=1, die2=6, streak=0)"
