# 01 — AuthN vs AuthZ & Identity Models: Gate, Badge & Family Register

## 1. The two gates (say this first in interviews)

- **AuthN (authentication)** = "WHO are you?" — prove identity (password, OTP, passkey, Google login).
- **AuthZ (authorization)** = "WHAT may you do?" — permissions (asha may *read* bills, only manager may *refund*).
- Real world: office gate checks ID card (AuthN), then room locks decide which doors open (AuthZ). Mixing them = `if logged_in: allow_refund()` — the classic IDOR factory.

## 2. Credential styles (badge shelf)

| Style | How | Use / caution |
|---|---|---|
| HTTP Basic | `Authorization: Basic base64(user:pass)` per request | legacy/internal only + HTTPS (else postcard readable); browsers cache annoyingly |
| API key | `X-API-Key: ...` or query | service-to-service, low-risk reads; rotate easily, scope narrowly; NEVER in frontend JS |
| Bearer token (JWT/opaque) | `Authorization: Bearer <token>` | user sessions for APIs; short-lived + refresh (see `02-jwt.md`) |
| Session cookie | `Set-Cookie: session=...; HttpOnly; Secure` | browser apps; server stores state (Redis) — revocation is instant (`DEL session`) |

Stateless JWT (no lookup, scales) vs stateful session/opaque (lookup, instant revoke) — the eternal trade. Most GenAI backends: **short JWT (5–15 min) + rotating refresh in HttpOnly cookie**.

## 3. Stronger doors: MFA & passwordless

- **MFA**: password + TOTP (authenticator app, RFC 6238: `HMAC(secret, 30s-counter)`) or SMS (SIM-swap risk!) or WebAuthn/passkeys (phishing-proof public-key — the future).
- **Passwordless**: magic link (short-lived signed token to email), OTP, passkeys. Still bind to a verified identifier + rate-limit attempts (topic 02's bucket!).

## 4. Enterprise directory (know the nouns)

- **SSO**: login once → many apps (via OIDC/SAML below, e.g. "Login with Google/Microsoft").
- **OIDC** = OAuth2 + `id_token` (JWT saying *who*: `sub`, `email_verified`) — modern web SSO.
- **SAML** = XML assertions via browser redirects — legacy enterprise SSO (still in banks/govt).
- **LDAP/AD** = company phonebook protocol (read attributes/groups); **Kerberos** = ticket-based intranet auth (Windows domains; `kinit` gets TGT, services get service tickets — no passwords on wire).
- **IdPs**: Keycloak (self-hosted, free), Auth0/Okta, Entra ID (Azure), Cognito (AWS). Your app = "relying party": redirect → IdP → callback with code → tokens. Never build password storage when an IdP exists (build-vs-buy!).

One-liners: **"AuthN proves who, AuthZ decides what." / "Short access + rotating refresh; sessions for browsers, bearer for APIs; SSO via OIDC (new) / SAML (legacy)."**
Runnable: login + RBAC API in `../examples/03_auth_api.py`.
