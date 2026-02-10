# SDET Live Technical Exercise (UI + API) — Starter Repo

This repo contains a tiny local e-commerce site (Flask) **plus** a small API.  
It is designed for a live interview exercise: automate a simple purchase flow and discuss test design.

## What the candidate will do (during the interview)
1. Walk through the purchase flow (UI).
2. Implement/extend UI automation for the flow (product → cart → checkout → pay).
3. Implement/extend API tests (validate cart/order via API).
4. Explain test cases, validations, structure, and trade-offs.

> Goal: evaluate approach and reasoning, not “perfect production code”.

---

## Prerequisites (candidate should prepare before interview)
- Python 3.10+ (3.11 recommended)
- A working local automation environment
- Chrome installed (or Chromium)

---

## Quickstart

### 1) Create and activate venv
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 2) Install dependencies
```bash
python -m pip install -r requirements.txt 
```

### 3) Run the demo web app (in one terminal)
```bash
python -m app
```
Open: http://127.0.0.1:5000

### 4) Run tests (in another terminal)
```bash
pytest -q
```

---

## Test card details (for the UI flow)
The payment page accepts **test cards only**:
- Card number: `4242 4242 4242 4242`
- Exp: any future date (e.g., 12/30)
- CVC: any 3 digits (e.g., 123)

Invalid cards will be rejected, e.g. `4000 0000 0000 0002`.

---

## Where to work
- UI tests: `tests/ui/`
- API tests: `tests/api/`

The provided tests include a **smoke test** to validate the environment,
and **skeleton tests** where the candidate can implement the purchase flow.

---

## Notes for interviewers
- Default base URL: `http://127.0.0.1:5000`
- This exercise intentionally includes a couple of mildly dynamic UI behaviors:
  - async cart total recalculation
  - coupon validation
  - shipping option changes total
These are meant to prompt discussion around waits, flakiness, selectors, and assertions.

