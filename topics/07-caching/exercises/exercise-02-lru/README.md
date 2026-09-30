# Exercise 02 — Who Flies Out? (O(1) LRU)

**Story:** Implement the eviction interview classic from scratch — no `lru_cache` allowed.

## Task
In `solution.py`, `LRU(cap)` with `get(k)` (→ value/`None`, marks recent) and `put(k, v)` (insert/update, evict least-recent past cap). Aim O(1) via `OrderedDict`.

## Acceptance
- cap=2: put a,b → get a → put c evicts b (not a); update refreshes; get missing → None
