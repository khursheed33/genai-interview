# Exercise 02 — Postman Patterns (topic routing `*` and `#`)

**Story:** `order.paid.blr` must reach blr-queue AND audit; `order.#` must catch long tails. Implement matching.

## Task
In `solution.py`, `match(pattern, key)` → bool: `*` = exactly one word, `#` = rest (may be last; support mid-`#` too: segments must align around it).

## Acceptance
- `order.*.blr` ✓ `order.paid.blr`, ✗ `order.paid.del`, ✗ `order.paid.blr.x`
- `order.#` ✓ both short and long tails; `#` alone ✓ everything
