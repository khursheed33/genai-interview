# Exercise 01 — Lazy Tiffin + Expiry Slip (aside + TTL)

**Story:** Menu reads hammer Postgres. Add aside-cache with TTL; writes must delete, not update.

## Task
In `solution.py` implement `AsideCache(db: dict, clock)`:
- `get(k, ttl=60)` → value (hit) or fetch from `db`, store with deadline, return it; count `hits`/`misses`
- `set(k, v)` → write `db` + DELETE cached key (return nothing)

## Acceptance
- miss→hit sequence counts 1/1; write deletes (next get re-misses); expired key re-misses (fake clock)
