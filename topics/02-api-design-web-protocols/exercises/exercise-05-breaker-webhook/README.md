# Exercise 05 — Fuse Box + Secret Knock (breaker + webhook HMAC)

**Story:** Payment provider flaps. Checkout must fail fast with a fallback, then auto-recover. Meanwhile Razorpay-style webhooks need forgery-proof verification.

## Task
In `solution.py`:
- `Breaker(clock, threshold=3, open_secs=10)` with `.call(fn, fallback)` — closed→open after `threshold` fails; open fails fast until `open_secs` pass; then half-open single probe (success→closed, fail→open).
- `sign(secret: bytes, body: bytes) -> str` + `verify(secret, body, sig) -> bool` using HMAC-SHA256 + `compare_digest`.

## Acceptance
- 3 failing calls → state `open`; calls during open return fallback WITHOUT invoking `fn`
- After `open_secs`, a succeeding probe → `closed`
- `verify` true for genuine body+sig, false for tampered body
