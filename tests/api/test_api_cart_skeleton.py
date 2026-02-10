import pytest
import requests

pytestmark = pytest.mark.api

def test_api_cart_add_and_totals__IMPLEMENT_ME(base_url):
    """
    Candidate task (API):
      - Fetch products
      - Add an item to cart via POST /api/cart/items
      - Verify totals (subtotal/total) are consistent
      - Optionally remove item and verify cart empty

    Discuss:
      - What would you validate (schema, status codes, idempotency, contract)?
      - How would you handle test data isolation (sessions, state reset)?
    """
    raise NotImplementedError
