import pytest
from moneypoly.cards import CardDeck

def test_carddeck_init():
    cards = [{"id": 1}, {"id": 2}]
    deck = CardDeck(cards)
    assert len(deck) == 2
    assert deck.index == 0

def test_carddeck_draw():
    cards = [{"id": 1}, {"id": 2}]
    deck = CardDeck(cards)
    assert deck.draw() == {"id": 1}
    assert deck.index == 1
    assert deck.draw() == {"id": 2}
    assert deck.index == 2

def test_carddeck_draw_exhausted():
    cards = [{"id": 1}]
    deck = CardDeck(cards)
    deck.draw() # index 1
    assert deck.draw() == {"id": 1}
    assert deck.index == 2

def test_carddeck_empty_draw():
    deck = CardDeck([])
    assert deck.draw() is None

def test_carddeck_peek():
    cards = [{"id": 1}, {"id": 2}]
    deck = CardDeck(cards)
    assert deck.peek() == {"id": 1}
    assert deck.index == 0 # unchanged

def test_carddeck_empty_peek():
    deck = CardDeck([])
    assert deck.peek() is None

def test_carddeck_reshuffle():
    cards = [{"id": 1}, {"id": 2}]
    deck = CardDeck(cards)
    deck.index = 5
    deck.reshuffle()
    assert deck.index == 0

def test_carddeck_cards_remaining():
    cards = [{"id": 1}, {"id": 2}, {"id": 3}]
    deck = CardDeck(cards)
    assert deck.cards_remaining() == 3
    deck.draw()
    assert deck.cards_remaining() == 2

def test_carddeck_repr():
    cards = [{"id": 1}, {"id": 2}]
    deck = CardDeck(cards)
    assert repr(deck) == "CardDeck(2 cards, next=0)"
