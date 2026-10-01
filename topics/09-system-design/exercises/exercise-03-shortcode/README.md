# Exercise 03 — Collision-Free Codes (base62 + allocator)

**Story:** Hash-based codes collide at 1M URLs. Switch to counter + base62.

## Task
In `solution.py`:
- `encode(n)` / `decode(s)` — base62 roundtrip (`0-9a-zA-Z`)
- `Allocator(start)` with `.next()` → monotonic ints (range-grab simulation: each `next()` +1 from start)

## Acceptance
- Roundtrip 0, 61, 62, 123456789; `encode` uses only alphabet chars; allocator strictly increasing from start+1
