# Exercise 01 — Rank the Regulars (CTE + window)

**Story:** Marketing wants top spenders (paid only!) with ranks + grand total, one query.

## Task
In `solution.py`, `top_spenders(conn)` runs a CTE + `RANK() OVER` + `SUM() OVER ()` over the given `users`/`orders` schema (seed helper `seed()` provided) and returns `[(name, total, rnk, grand)]` ordered by rank.

## Acceptance
- Paid-only totals; ranks 1..N dense-correct; grand = sum of totals; `cara` (no paid orders) absent
