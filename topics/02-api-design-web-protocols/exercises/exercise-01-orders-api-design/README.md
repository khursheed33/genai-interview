# Exercise 01 — Design the Orders Menu (REST conventions)

**Story:** Your startup's orders API looks like `GET /getOrder?id=1` and `POST /createOrder`. The mobile team is crying. Redesign it.

## Task
In `solution.py` fill `ROUTES` — a list of `{method, path, status}` dicts covering: create order, get one, list (paginated), full replace, partial update, cancel. Use `STATUS` helper already there.

## Acceptance
- No verbs in paths (`/getOrder`, `/createOrder` forbidden); collections plural (`/orders`)
- Create → `POST /orders` + `201`; get → `GET /orders/{id}` + `200`; replace → `PUT`; partial → `PATCH`; cancel → `DELETE`
- Run: `uv run pytest topics/02-api-design-web-protocols/exercises/exercise-01-orders-api-design -q`
