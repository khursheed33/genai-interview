# Exercise 03 — Librarian's Counter (repo + no N+1 + 409)

**Story:** Handlers run raw SQL and the users loop fires 51 queries. Replace with a repo.

## Task
In `solution.py` (SQLite in-memory, models given) implement `UserRepo(db)`:
- `create(name, email)` → id (commit; duplicate email raises `IntegrityError`)
- `get(uid)` → `{"id", "name", "email"}` or `None`
- `list_with_orders()` → list of `{"name", "n_orders"}` using ONE eager query (`selectinload`)

Also implement `to_status(exc)` → `409` for `IntegrityError`, else `500`.

## Acceptance
- Roundtrip create→get works; duplicate email raises and maps to `409`
- `list_with_orders()` correct counts AND runs ≤ 2 SQL statements (counter in test)
