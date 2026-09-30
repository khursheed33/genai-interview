# Exercise 05 — Paraphrase Piggybank (normalize + semantic threshold)

**Story:** Support bot burns $40/day re-answering "refund policy?" phrased 50 ways. Cache meaning, not spelling.

## Task
In `solution.py`:
- `normalize(q)` → strip + lowercase + collapse spaces + drop trailing `?!.,`
- `jaccard(a, b)` on word sets; `SemanticCache(threshold=0.5)` with `put(q, ans)` / `ask(q)` → `(answer, "exact"|"semantic(x.xx)"|"miss")`

## Acceptance
- `"  Refund Policy?! "` normalizes equal to `"refund policy"`; paraphrase ≥ threshold hits semantic; unrelated misses; prices never pre-cached (test asserts miss)
