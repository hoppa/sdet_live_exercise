## API tests

Suggested checks:
- /api/health returns ok
- /api/products list is non-empty
- Add items to /api/cart/items and verify totals
- /api/checkout validates cart
- After a successful UI purchase, /api/orders/last matches expected status/totals
