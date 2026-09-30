# Exercise 01 — Grinder Settings (salted hashes + rehash)

**Story:** Users table leaked (hashed, phew). But two users with `dosa123` have IDENTICAL hashes — no salt! And cost is 10k iterations from 2019. Fix both.

## Task
In `solution.py` (stdlib only):
- `hash_pw(password, salt=None, iters=ITERS)` → `"pbkdf2$<iters>$<salt_hex>$<hash_hex>"` (random 16B salt when omitted)
- `verify(password, stored)` → bool via `hmac.compare_digest`
- `needs_rehash(stored)` → True when stored iters < current `ITERS`

## Acceptance
- Same password twice → different hashes; `verify` true/false correctly
- Legacy `iters=10_000` hash → `needs_rehash` True; fresh → False
