# 02 — JWT: Sealed Tiffin Slip (HS256 vs RS256, refresh, revoke)

## 1. Anatomy: `header.payload.signature` (base64url × 3)

```
eyJhbGciOiJIUzI1NiJ9 . eyJzdWIiOiIxMjMifQ . SflKxwRJ...   (decode the middle on jwt.io!)
```

- **Header**: `{"alg":"HS256","typ":"JWT"}`. **Payload**: claims — `sub` (user id), `iat/exp` (times), `iss/aud` (who made/for whom), `jti` (unique id — revocation handle!), `scope/roles`.
- **Signature**: `HMAC(secret, header.payload)` (HS256) or `RSA-sign(private_key, ...)` (RS256). Anyone can READ; only key-holder can SEAL. Tamper `sub:"123"→"1"` (admin) → signature mismatch → rejected. Demo in `../examples/02_jwt_hs_rs.py`.

## 2. HS256 vs RS256 (shared secret vs seal-stamp)

| | HS256 | RS256 (prod default for multi-service) |
|---|---|---|
| Key | ONE shared secret (server holds) | private signs (auth service) / MANY verify with public (gateway, 5 microservices) |
| Risk | secret leaks anywhere = forge everywhere | private stays in KMS/HSM; publics are public |
| Rotation | painful (all verifiers same day) | publish `jwks.json` with `kid`s, overlap old+new |

Rules: `exp` SHORT (5–15 min access), `aud`+`iss` checked (don't accept gym tokens at bank!), `alg` whitelisted (kill the `alg:none` attack — never trust header's word), clock skew `±60s`.

## 3. Refresh flow (stay logged in WITHOUT 30-day access tokens)

```
login → [access 10min] + [refresh 7d in HttpOnly cookie]
access dies → POST /refresh {refresh} → ROTATE: new pair + REVOKE old jti (reuse = theft alert!)
logout → blocklist both jtis (Redis SETEX till exp)
```

- **Rotation**: each refresh mints a NEW refresh and kills the old. Stolen refresh reused → already dead → alarm + kill session family. 
- **Revocation**: JWTs can't be "un-signed" — keep a `revoked_jtis` set (Redis, TTL = exp). Check it in the auth dep (one fast lookup; still stateless-ish).
- Mobile: refresh in secure storage + app-attest; web: HttpOnly+Secure+SameSite cookie (XSS can't steal, CSRF needs SameSite+token).

One-liner: **"Short access, rotating refresh, jti blocklist; RS256 via JWKS; never trust `alg`, always check `exp/aud/iss`."**
