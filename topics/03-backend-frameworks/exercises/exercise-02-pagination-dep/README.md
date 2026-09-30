# Exercise 02 — Page Dep That Says No (capped pagination)

**Story:** `GET /orders?limit=1000000` just melted staging. Build a bouncer.

## Task
In `solution.py` implement:
- `clamp_limit(limit, maximum=100)` → `min(max(limit, 1), maximum)`
- `paginate(items, limit=20, offset=0)` → `{"data": slice, "total": len(items)}` using the clamp (default max 100)

## Acceptance
- `clamp_limit(10**6) == 100`, `clamp_limit(-5) == 1`
- `paginate(list(range(50)), limit=5, offset=10)["data"] == [10, 11, 12, 13, 14]`, `total == 50`
