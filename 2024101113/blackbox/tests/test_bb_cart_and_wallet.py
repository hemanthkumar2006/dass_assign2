import pytest
import requests
from conftest import BASE_URL, HEADERS, skip_if_no_server

@skip_if_no_server
def test_cart_add_negative_quantity_returns_400():
    """quantity must be >= 1; sending -5 must return HTTP 400."""
    payload = {"product_id": 1, "quantity": -5}
    resp = requests.post(f"{BASE_URL}/cart/add", headers=HEADERS, json=payload)
    assert resp.status_code == 400, f"Expected 400 for negative quantity, got {resp.status_code}"

@skip_if_no_server
def test_cart_add_zero_quantity_returns_400():
    """quantity = 0 is also invalid -> boundary value test."""
    payload = {"product_id": 1, "quantity": 0}
    resp = requests.post(f"{BASE_URL}/cart/add", headers=HEADERS, json=payload)
    assert resp.status_code == 400, f"Expected 400 for zero quantity, got {resp.status_code}"

@skip_if_no_server
def test_wrong_type_product_id_in_cart():
    """product_id must be an integer; sending a string should return 400."""
    payload = {"product_id": "abc", "quantity": 1}
    resp = requests.post(f"{BASE_URL}/cart/add", headers=HEADERS, json=payload)
    assert resp.status_code == 400, f"Expected 400 for non-integer product_id"

@skip_if_no_server
def test_wallet_add_exceeds_limit_returns_400():
    """Wallet top-up must not exceed 100,000; exceeding it should return 400."""
    payload = {"amount": 100001}
    resp = requests.post(f"{BASE_URL}/wallet/add", headers=HEADERS, json=payload)
    assert resp.status_code == 400, f"Expected 400 for wallet top-up exceeding limit"

@skip_if_no_server
def test_cart_total_includes_last_item():
    """Bug 1: Cart total must include ALL items, including the last one added."""
    # Clear cart first, then add two items
    requests.delete(f"{BASE_URL}/cart", headers=HEADERS)
    requests.post(f"{BASE_URL}/cart/add", headers=HEADERS, json={"product_id": 1, "quantity": 1})
    requests.post(f"{BASE_URL}/cart/add", headers=HEADERS, json={"product_id": 2, "quantity": 1})

    resp = requests.get(f"{BASE_URL}/cart", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    items = data.get("items", [])
    expected_total = sum(item["subtotal"] for item in items)
    actual_total = data.get("total", None)
    assert actual_total == expected_total, (
        f"Bug 1: Cart total mismatch - expected {expected_total}, got {actual_total}"
    )

@skip_if_no_server
def test_checkout_card_payment_status_is_paid():
    """Bug 4: CARD payments should start as PAID, not PENDING."""
    resp = requests.post(
        f"{BASE_URL}/checkout",
        headers=HEADERS,
        json={"payment_method": "CARD"}
    )
    assert resp.status_code in (200, 201)
    order = resp.json()
    assert order.get("payment_status") == "PAID", (
        f"Bug 4: Expected payment_status='PAID' for CARD, got '{order.get('payment_status')}'"
    )

@skip_if_no_server
def test_wallet_pay_exact_deduction():
    """Bug 5: Wallet pay must deduct exactly the requested amount, no more."""
    # Get current balance
    balance_resp = requests.get(f"{BASE_URL}/wallet", headers=HEADERS)
    assert balance_resp.status_code == 200
    old_balance = balance_resp.json().get("balance")

    deduct_amount = 50
    pay_resp = requests.post(
        f"{BASE_URL}/wallet/pay",
        headers=HEADERS,
        json={"amount": deduct_amount}
    )
    assert pay_resp.status_code == 200

    new_balance_resp = requests.get(f"{BASE_URL}/wallet", headers=HEADERS)
    new_balance = new_balance_resp.json().get("balance")
    assert new_balance == old_balance - deduct_amount, (
        f"Bug 5: Expected balance {old_balance - deduct_amount}, got {new_balance}"
    )
