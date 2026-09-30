# 03 — OAuth 2.0 & OIDC: Valet Key Ceremony (PKCE included)

OAuth2 = **delegation** ("let Swiggy read my Google contacts WITHOUT my Google password"). OIDC adds **identity** ("and here's a signed slip saying who I am").

## 1. Roles in one line

**Resource Owner** (you) → **Client** (Swiggy app) → **Authorization Server** (Google login) → **Resource Server** (contacts API). Tokens: `access_token` (short, calls APIs) + optional `refresh_token`.

## 2. Grant types (which ceremony when?)

| Grant | Story | Use |
|---|---|---|
| **Auth code + PKCE** | Valet takes your car-key-copy, returns car only to key-holder | ALL user-facing apps now (web/mobile/SPA) — THE default |
| Client credentials | Two robots shake hands (`client_id:secret` → token) | service-to-service (billing → email API), scopes narrow |
| Device code | TV shows `ABCD-1234`, you approve on phone | TVs/CLIs with no keyboard |
| (Legacy: implicit/password grants — DEAD, don't use: tokens in URL, password sharing) |

## 3. PKCE walkthrough (S256) — defeats code interception on mobile

```
app: verifier = random(43-128 chars); challenge = base64url(sha256(verifier))
1. app → auth server: /authorize?...&code_challenge=<C>&code_challenge_method=S256
2. user logs in, approves → server returns one-time `code` (bound to C)
3. app → /token {code, code_verifier=<V>}  → server: sha256(V)==C? mint tokens : reject
```

Attacker stealing `code` lacks `V` → useless. Verifier lives in app memory only. Demo generators in `../examples/04_oauth_pkce.py`.

## 4. Scopes = least privilege slips (`read:orders`, `refund:payments`)

Request minimal (`openid profile email` for login; `refund:*` NEVER for frontend). Server ENFORCES per-endpoint (`require("orders:read")`); frontend hiding buttons is UX, not security. Wildcard `*` scopes = junior mistake.

## 5. OIDC in 3 claims

After code → tokens, `id_token` (JWT) says: `sub` (stable user id — key your DB on THIS, not email!), `email_verified`, `iss/aud/exp` checked, `nonce` matched (replay guard). Logout = kill app session + redirect to IdP logout (else SSO silently re-logs-in — spooky interviews love this).

One-liner: **"Auth-code+PKCE for users, client-credentials for robots, scopes minimal + enforced server-side, key users by `sub`."**
