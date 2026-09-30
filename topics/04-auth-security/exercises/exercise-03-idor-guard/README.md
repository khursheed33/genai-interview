# Exercise 03 — Whose Order Is It? (IDOR guard + policy)

**Story:** `GET /orders/7` returns ANYONE's order. Bob just read Asha's refund. Fix the object check.

## Task
In `solution.py` (store `ORDERS = {id: {"owner": ..., "region": ..., "amount": ...}}` given):
- `authorize(current: {"id", "roles"}, oid)` → `(status, order_or_None)`: 404 if missing; 200 if owner or `admin` in roles; else 403
- `may_refund(user: {"role", "region"}, order, hour)` → bool: manager/admin + same region + amount ≤ 10000 + 9 ≤ hour < 18

## Acceptance
- Owner 200, stranger 403, admin 200, ghost 404; refund policy true only when ALL conditions hold (4 negative cases)
