# Exercise 02 — Size the Bouncer's Memory (bloom m/k + verify)

**Story:** Crawler dedupes 1M URLs at 1% FP. How many bits? How many hashes? Prove empirically.

## Task
In `solution.py`:
- `bits(n, p)` → int (ceil of `-n ln p / (ln2)²`); `hashes(m, n)` → int ≥1 (round of `m/n ln2`)
- `Bloom(n, p)` class with `add` + `__contains__` (double-hashing, bytearray)

## Acceptance
- `bits(1M, 0.01)` ≈ 9.6M; `hashes` == 7; 500 adds → all found (no false negatives); 2000 absent → FP rate < 5%
