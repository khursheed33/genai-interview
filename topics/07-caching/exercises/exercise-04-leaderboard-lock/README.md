# Exercise 04 — Rank + Badge (zset leaderboard + token lock, fakeredis)

**Story:** Game week: live leaderboard + one-chef-at-a-time payout job. Both on Redis.

## Task
In `solution.py` (fakeredis client passed in):
- `add_score(r, board, user, pts)` → new total (ZINCRBY); `top(r, board, n)` → list of `(user, score)` best-first (decode bytes!)
- `acquire(r, key, ttl_ms=5000)` → token or `None` (SET NX PX); `release(r, key, token)` → True only if token matches (GET-compare-DEL)

## Acceptance
- Totals accumulate; top-2 ordered desc; double-acquire blocked; wrong-token release False; right-token True + free
