import pytest

pytestmark = pytest.mark.ui

def test_purchase_flow_happy_path__IMPLEMENT_ME():
    """
    Candidate task (UI):
      - Open /products
      - Add a product to cart
      - Update cart (optionally apply coupon + change shipping)
      - Proceed to checkout
      - Fill form + pay with success card
      - Assert success page + order id + status

    Notes:
      - Use `data-testid` selectors where possible.
      - Discuss waits and async totals refresh (app.js).
      - Keep it readable: helpers/page objects are OK but not required.
    """
    raise NotImplementedError
