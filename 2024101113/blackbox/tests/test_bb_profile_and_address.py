import pytest
import requests
from conftest import BASE_URL, HEADERS, ADMIN_HEADERS, skip_if_no_server

@skip_if_no_server
def test_admin_users_returns_200():
    """Valid admin request should return HTTP 200 with a list of users."""
    resp = requests.get(f"{BASE_URL}/admin/users", headers=ADMIN_HEADERS)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list), "Response body should be a list"

@skip_if_no_server
def test_profile_update_invalid_phone_returns_400():
    """Phone must be exactly 10 digits; a 3-digit phone should be rejected."""
    payload = {"name": "Alice", "phone": "123"}
    resp = requests.put(f"{BASE_URL}/profile", headers=HEADERS, json=payload)
    assert resp.status_code == 400, f"Expected 400 for invalid phone, got {resp.status_code}"

@skip_if_no_server
def test_address_street_too_long_returns_400():
    """Street field longer than 100 characters should return 400."""
    long_street = "A" * 101
    payload = {"street": long_street, "city": "Anytown", "pincode": "123456"}
    resp = requests.post(f"{BASE_URL}/addresses", headers=HEADERS, json=payload)
    assert resp.status_code == 400, f"Expected 400 for long street, got {resp.status_code}"

@skip_if_no_server
def test_address_pincode_boundary_exact_6_digits():
    """Pincode must be exactly 6 digits; test boundary value."""
    payload = {"street": "Main St", "city": "Anytown", "pincode": "123456"}
    resp = requests.post(f"{BASE_URL}/addresses", headers=HEADERS, json=payload)
    assert resp.status_code in (200, 201), "Valid 6-digit pincode should succeed"

@skip_if_no_server
def test_missing_x_roll_number_header_returns_400():
    """Requests without X-Roll-Number header should be rejected."""
    resp = requests.get(f"{BASE_URL}/admin/users")  # no headers at all
    assert resp.status_code in (400, 401), (
        f"Expected 400/401 when X-Roll-Number is missing, got {resp.status_code}"
    )

@skip_if_no_server
def test_missing_x_user_id_for_user_endpoint_returns_401():
    """User-scoped endpoints require X-User-ID; omitting it should return 401."""
    resp = requests.get(f"{BASE_URL}/profile", headers=ADMIN_HEADERS)  # no X-User-ID
    assert resp.status_code in (400, 401), (
        f"Expected 400/401 when X-User-ID is missing, got {resp.status_code}"
    )

@skip_if_no_server
def test_address_update_returns_new_data():
    """Bug 2: PUT address must return the NEW address data, not the old snapshot."""
    # Create an address first
    create_resp = requests.post(
        f"{BASE_URL}/addresses",
        headers=HEADERS,
        json={"street": "Old Street", "city": "OldCity", "pincode": "000000"}
    )
    assert create_resp.status_code in (200, 201)
    address_id = create_resp.json().get("id")

    new_street = "4th New Street"
    update_resp = requests.put(
        f"{BASE_URL}/addresses/{address_id}",
        headers=HEADERS,
        json={"street": new_street, "is_default": True}
    )
    assert update_resp.status_code == 200
    returned = update_resp.json()
    assert returned.get("street") == new_street, (
        f"Bug 2: Response returned old street '{returned.get('street')}', expected '{new_street}'"
    )
