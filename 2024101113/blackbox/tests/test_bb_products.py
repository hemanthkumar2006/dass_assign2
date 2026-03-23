import pytest
import requests
from conftest import BASE_URL, HEADERS, skip_if_no_server

@skip_if_no_server
def test_get_products_returns_200():
    """Fetching all products is a basic valid request and must succeed."""
    resp = requests.get(f"{BASE_URL}/products", headers=HEADERS)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

@skip_if_no_server
def test_review_rating_above_five_returns_400():
    """Rating > 5 is out of range and must be rejected with 400."""
    payload = {"product_id": 1, "rating": 6, "comment": "Too good!"}
    resp = requests.post(f"{BASE_URL}/products/1/reviews", headers=HEADERS, json=payload)
    assert resp.status_code == 400, f"Expected 400 for rating 6, got {resp.status_code}"

@skip_if_no_server
def test_review_rating_average_is_decimal():
    """Bug 3: Average rating must be a float, not a truncated integer."""
    # Post two ratings: 4 and 5 -> average should be 4.5
    requests.post(
        f"{BASE_URL}/products/1/reviews", headers=HEADERS,
        json={"rating": 4, "comment": "Good"}
    )
    requests.post(
        f"{BASE_URL}/products/1/reviews", headers=HEADERS,
        json={"rating": 5, "comment": "Great"}
    )
    resp = requests.get(f"{BASE_URL}/products/1/reviews", headers=HEADERS)
    assert resp.status_code == 200
    avg = resp.json().get("average_rating")
    assert isinstance(avg, float), f"Bug 3: average_rating should be float, got {type(avg)}"
    assert avg != int(avg) or avg == 5.0, (
        f"Bug 3: average_rating appears truncated to integer: {avg}"
    )
