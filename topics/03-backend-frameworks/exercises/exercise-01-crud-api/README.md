# Exercise 01 — Tiny Orders API (routes + guard + gift pack)

**Story:** The dhaba needs an orders counter: create, fetch, 404 for ghosts, 422 for empty tiffins.

## Task
In `solution.py`, `build_app()` must wire a FastAPI app with in-memory store exposing:
- `POST /orders` → `201` (`OrderOut`), invalid body → `422`
- `GET /orders/{oid}` → `200`, unknown → `404` with `{"title": ...}` body

`OrderIn`/`OrderOut` are given — keep them.

## Acceptance
`uv run pytest topics/03-backend-frameworks/exercises/exercise-01-crud-api -q` — create→201, get→200, ghost→404, empty items→422.
