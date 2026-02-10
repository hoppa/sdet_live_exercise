from __future__ import annotations

import uuid
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional

from flask import Flask, jsonify, render_template, request, redirect, url_for, session

# -------------------------
# In-memory "database"
# -------------------------

@dataclass
class Product:
    id: str
    name: str
    price_cents: int

PRODUCTS: List[Product] = [
    Product(id="p1", name="Travel Mug", price_cents=1599),
    Product(id="p2", name="Laptop Stand", price_cents=3999),
    Product(id="p3", name="Noise-Cancel Headphones", price_cents=12999),
]

COUPONS = {
    "SAVE10": 0.10,
    "SAVE20": 0.20,
}

SHIPPING = {
    "standard": 599,
    "express": 1499,
}

def cents_to_money(c: int) -> str:
    return f"{c/100:.2f}"

def get_cart() -> Dict[str, Any]:
    if "cart" not in session:
        session["cart"] = {"items": {}, "coupon": None, "shipping": "standard"}
    return session["cart"]

def cart_totals(cart: Dict[str, Any]) -> Dict[str, int]:
    subtotal = 0
    for pid, qty in cart["items"].items():
        prod = next((p for p in PRODUCTS if p.id == pid), None)
        if prod:
            subtotal += prod.price_cents * int(qty)
    shipping = SHIPPING.get(cart.get("shipping", "standard"), SHIPPING["standard"])
    discount_rate = COUPONS.get(cart.get("coupon") or "", 0.0)
    discount = int(round(subtotal * discount_rate))
    total = max(0, subtotal - discount) + shipping
    return {"subtotal": subtotal, "discount": discount, "shipping": shipping, "total": total}

def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "dev-secret-change-me"

    # -------------------------
    # UI Routes
    # -------------------------

    @app.get("/")
    def home():
        return redirect(url_for("products_page"))

    @app.get("/products")
    def products_page():
        return render_template("products.html", products=PRODUCTS)

    @app.post("/cart/add")
    def cart_add():
        pid = request.form.get("product_id")
        qty = int(request.form.get("qty", "1"))
        cart = get_cart()
        cart["items"][pid] = int(cart["items"].get(pid, 0)) + qty
        session["cart"] = cart
        return redirect(url_for("cart_page"))

    @app.get("/cart")
    def cart_page():
        cart = get_cart()
        totals = cart_totals(cart)
        # Denormalize items for display
        items = []
        for pid, qty in cart["items"].items():
            prod = next((p for p in PRODUCTS if p.id == pid), None)
            if prod:
                items.append({
                    "id": prod.id,
                    "name": prod.name,
                    "qty": int(qty),
                    "price": cents_to_money(prod.price_cents),
                    "line": cents_to_money(prod.price_cents * int(qty)),
                })
        return render_template(
            "cart.html",
            items=items,
            coupon=cart.get("coupon"),
            shipping=cart.get("shipping", "standard"),
            totals={k: cents_to_money(v) for k, v in totals.items()},
        )

    @app.post("/cart/update")
    def cart_update():
        cart = get_cart()
        items = dict(cart["items"])
        # Update quantities
        for key, val in request.form.items():
            if key.startswith("qty_"):
                pid = key.replace("qty_", "")
                try:
                    q = max(0, int(val))
                except ValueError:
                    q = 0
                if q == 0:
                    items.pop(pid, None)
                else:
                    items[pid] = q

        coupon = request.form.get("coupon") or None
        shipping = request.form.get("shipping") or "standard"
        cart["items"] = items
        cart["coupon"] = coupon
        cart["shipping"] = shipping
        session["cart"] = cart
        return redirect(url_for("cart_page"))

    @app.get("/checkout")
    def checkout_page():
        cart = get_cart()
        if not cart["items"]:
            return redirect(url_for("products_page"))
        totals = cart_totals(cart)
        return render_template(
            "checkout.html",
            totals={k: cents_to_money(v) for k, v in totals.items()},
        )

    @app.post("/pay")
    def pay():
        cart = get_cart()
        if not cart["items"]:
            return redirect(url_for("products_page"))

        name = request.form.get("name", "").strip()
        address = request.form.get("address", "").strip()
        card = re_digits(request.form.get("card", ""))
        exp = request.form.get("exp", "").strip()
        cvc = request.form.get("cvc", "").strip()

        errors = []
        if not name:
            errors.append("Name is required.")
        if not address:
            errors.append("Address is required.")
        if len(card) < 12:
            errors.append("Card number looks invalid.")
        if not exp:
            errors.append("Expiry is required.")
        if not cvc or not cvc.isdigit():
            errors.append("CVC is required.")

        # Simulated payment gateway behavior
        # - 4242... = approved
        # - 4000...0002 = declined
        approved = (card == "4242424242424242")
        declined = (card == "4000000000000002")

        if declined or (card and not approved):
            errors.append("Payment was declined (test gateway). Use 4242 4242 4242 4242 for success.")

        if errors:
            totals = cart_totals(cart)
            return render_template(
                "checkout.html",
                totals={k: cents_to_money(v) for k, v in totals.items()},
                errors=errors,
                form={"name": name, "address": address, "card": request.form.get("card",""), "exp": exp, "cvc": cvc},
            ), 400

        order_id = str(uuid.uuid4())[:8]
        totals = cart_totals(cart)
        order = {
            "id": order_id,
            "created_at": int(time.time()),
            "items": cart["items"],
            "coupon": cart.get("coupon"),
            "shipping": cart.get("shipping"),
            "totals": totals,
            "customer": {"name": name, "address": address},
            "status": "PAID",
        }
        session["last_order"] = order
        session["cart"] = {"items": {}, "coupon": None, "shipping": "standard"}
        return redirect(url_for("order_success", order_id=order_id))

    @app.get("/order/<order_id>")
    def order_success(order_id: str):
        order = session.get("last_order")
        if not order or order.get("id") != order_id:
            return redirect(url_for("products_page"))
        view = dict(order)
        view["totals"] = {k: cents_to_money(v) for k, v in order["totals"].items()}
        return render_template("success.html", order=view)

    # -------------------------
    # API Routes
    # -------------------------

    @app.get("/api/health")
    def api_health():
        return jsonify({"status": "ok"})

    @app.get("/api/products")
    def api_products():
        return jsonify({"products": [asdict(p) for p in PRODUCTS]})

    @app.get("/api/cart")
    def api_cart():
        cart = get_cart()
        totals = cart_totals(cart)
        return jsonify({"cart": cart, "totals": totals})

    @app.post("/api/cart/items")
    def api_cart_add():
        body = request.get_json(force=True, silent=True) or {}
        pid = body.get("product_id")
        qty = int(body.get("qty", 1))
        cart = get_cart()
        cart["items"][pid] = int(cart["items"].get(pid, 0)) + qty
        session["cart"] = cart
        return jsonify({"cart": cart, "totals": cart_totals(cart)}), 201

    @app.delete("/api/cart/items/<product_id>")
    def api_cart_remove(product_id: str):
        cart = get_cart()
        cart["items"].pop(product_id, None)
        session["cart"] = cart
        return jsonify({"cart": cart, "totals": cart_totals(cart)})

    @app.post("/api/checkout")
    def api_checkout():
        cart = get_cart()
        if not cart["items"]:
            return jsonify({"error": "cart_empty"}), 400
        totals = cart_totals(cart)
        return jsonify({"ready": True, "totals": totals})

    @app.get("/api/orders/last")
    def api_last_order():
        order = session.get("last_order")
        if not order:
            return jsonify({"error": "no_order"}), 404
        return jsonify({"order": order})

    return app

def re_digits(s: str) -> str:
    return "".join([c for c in (s or "") if c.isdigit()])
