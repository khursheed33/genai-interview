# Exercise 02 — Slips That Rotate (JWT + refresh + blocklist)

**Story:** Access tokens live 30 days. A stolen laptop means a month of admin access. Shorten + rotate + revoke.

## Task
In `solution.py` (PyJWT available):
- `mint(sub, roles, mins, secret)` → JWT with `sub/roles/iat/exp/jti`
- `verify(token, secret, revoked: set)` → claims dict, or `None` on expiry/tamper/revoked-jti
- `rotate(refresh_token, secret, revoked)` → `(new_access, new_refresh)` + adds old `jti` to `revoked`; returns `None` if input invalid

## Acceptance
- Roundtripokus; tampered → `None`; expired → `None`
- Rotated refresh works once; reuse → `None` (old jti dead); logout (add access jti) → `verify` `None`
