/**
 * Small dynamic behavior:
 * - When the user changes coupon/shipping/qty and clicks "Update",
 *   the server recalculates totals.
 * - Additionally, we simulate an async UI update after the page loads:
 *   totals get re-fetched from /api/cart and updated (like a SPA would).
 * This creates a bit of waiting/async behavior for UI automation.
 */
async function refreshTotals() {
  try {
    const res = await fetch("/api/cart", { headers: { "Accept": "application/json" }});
    if (!res.ok) return;
    const data = await res.json();
    const totals = data.totals || {};
    const money = (cents) => (cents/100).toFixed(2);

    const set = (id, value) => {
      const el = document.getElementById(id);
      if (el) el.textContent = "$" + value;
    };

    set("subtotal", money(totals.subtotal ?? 0));
    set("discount", money(totals.discount ?? 0));
    set("shippingFee", money(totals.shipping ?? 0));
    set("total", money(totals.total ?? 0));
  } catch (_) {
    // ignore
  }
}

window.addEventListener("load", () => {
  // Simulate async delay
  setTimeout(() => {
    refreshTotals();
  }, 450);
});
