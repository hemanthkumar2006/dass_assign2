import pytest
import requests

BASE_URL = "http://localhost:8080/api/v1"
HEADERS = {"X-Roll-Number": "2024101113", "X-User-ID": "1"}
ADMIN_HEADERS = {"X-Roll-Number": "2024101113"}

def _server_available():
    try:
        requests.get(f"{BASE_URL}/admin/users", headers=ADMIN_HEADERS, timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False

skip_if_no_server = pytest.mark.skipif(
    not _server_available(),
    reason="QuickCart server not available at localhost:8080"
)
