import pytest
import requests

pytestmark = pytest.mark.api

def test_api_health(base_url):
    r = requests.get(f"{base_url}/api/health", timeout=5)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
