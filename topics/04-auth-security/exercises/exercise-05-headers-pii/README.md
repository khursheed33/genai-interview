# Exercise 05 — Walls + Masks (headers + PII audit)

**Story:** ZAP flags missing CSP/HSTS; meanwhile support pasted a full card number into the ticket log. Ship both fixes.

## Task
In `solution.py`:
- `headers()` → dict with `Strict-Transport-Security`, `Content-Security-Policy` (containing `frame-ancestors 'none'`), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`
- `mask_email(e)` → `a***@dom`; `mask_card(n)` → `****1234`
- `audit(actor, action, obj, meta)` → same shape with `email*`/`card*` values masked (keys containing "email"/"card")

## Acceptance
- All 4 headers present, CSP has frame-ancestors; masks exact; audit masks only PII keys, keeps others
