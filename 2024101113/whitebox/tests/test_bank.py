import pytest
from moneypoly.bank import Bank
from moneypoly.player import Player

def test_bank_give_loan_deducts_funds():
    bank = Bank()
    player = Player("Alice", balance=0)
    initial_funds = bank.get_balance()
    amount = 500
    
    bank.give_loan(player, amount)
    
    # Needs to check if bank funds decreased by the loan amount
    assert bank.get_balance() == initial_funds - amount
    assert player.balance == amount

def test_bank_payout_insufficient_funds():
    bank = Bank()
    with pytest.raises(ValueError):
        bank.pay_out(bank.get_balance() + 100)

def test_bank_init():
    bank = Bank()
    assert bank.get_balance() > 0

def test_bank_pay_out_success():
    bank = Bank()
    amount = 500
    initial = bank.get_balance()
    bank.pay_out(amount)
    assert bank.get_balance() == initial - amount

def test_bank_collect_positive():
    bank = Bank()
    amount = 500
    initial = bank.get_balance()
    bank.collect(amount)
    assert bank.get_balance() == initial + amount

def test_bank_repr():
    bank = Bank()
    assert "Bank" in repr(bank)
