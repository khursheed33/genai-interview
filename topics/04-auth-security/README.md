# 04 - Authentication, Authorization and Security

> Scope: README.md section 4: AuthN/Z, JWT, OAuth2/OIDC/SAML, RBAC/ABAC, TLS/mTLS, hashing/encryption/KMS, OWASP Top 10 + API + LLM
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- Models → `notes/01-authn-authz-models.md` (AuthN vs AuthZ, badges, MFA/passkeys, SSO/OIDC/SAML/LDAP)
- JWT → `notes/02-jwt.md` (3 parts, HS vs RS, refresh rotation, jti revoke)
- OAuth → `notes/03-oauth2-oidc.md` (grants, PKCE ceremony, scopes, id_token)
- Access → `notes/04-access-control.md` (RBAC/ABAC/ACL, OPA, IDOR guard)
- Crypto → `notes/05-crypto-tls.md` (hash vs enc vs encoding, salts, envelope/KMS, TLS/mTLS)
- OWASP → `notes/06-owasp.md` (API 10 + classics, thief→lock table)
- Defenses → `notes/07-app-defenses.md` (headers/CSP, validation, WAF, SAST/SCA, audit)
- Privacy → `notes/08-privacy-llm-zerotrust.md` (PII/GDPR, LLM Top 10, zero trust, compliance)

## Examples (8 runnable — verified)
| File | Covers | Run |
|---|---|---|
| `examples/01_password_hashing.py` | PBKDF2 salt+pepper, timing-safe, rehash | `uv run python topics/04-auth-security/examples/01_password_hashing.py` |
| `examples/02_jwt_hs_rs.py` | HS256 + RS256, tamper/expiry/alg rejected | same pattern |
| `examples/03_auth_api.py` | login/refresh-rotate/logout, 401/403 via TestClient | same pattern |
| `examples/04_oauth_pkce.py` | verifier/challenge, single-use code, scopes | same pattern |
| `examples/05_rbac_abac.py` | role matrix, refund rulebook, IDOR guard | same pattern |
| `examples/06_injection_defenses.py` | SQLi/XSS/traversal/SSRF/CMDi blocked | same pattern |
| `examples/07_security_headers.py` | CSP/HSTS set, PII-masked audit | same pattern |
| `examples/08_auth_client.js` | Bearer auto-refresh + PKCE (node:crypto) | `node .../08_auth_client.js` |

## Exercises (5 — `uv run pytest topics/04-auth-security/exercises -q`, 10 tests)
- `exercise-01-passwords` — salted hash + verify + rehash
- `exercise-02-jwt-rotation` — mint/verify/rotate/reuse-dead
- `exercise-03-idor-guard` — owner-or-admin + refund policy
- `exercise-04-injection-guards` — 5 thieves, 5 locks
- `exercise-05-headers-pii` — headers + masks + audit

## Structure
- `README.md` - this checklist entry point
- `notes/` - your condensed notes (add `.md` per sub-topic)
- `examples/` - runnable minimal examples (python/js/sh)
- `exercises/` - practice tasks + solutions
- `interview-questions.md` - Q and A bank

## How to use
1. Read the checklist item in root README.
2. Add notes + code + diagrams here.
3. Do 2-3 exercises and 1 mini-project link in `projects/` if applicable.
4. Self-quiz with interview questions.

## Resources
- Add links as you learn (docs, papers, videos).
- Prefer primary sources: official docs, RFCs, papers.

## Progress
- [x] Notes drafted (8 files, gate/badge/thief stories)
- [x] Examples run (8 files, verified: PyJWT/RS256 + TestClient + node)
- [x] Exercises done (5 exercises, 10 pytest tests green)
- [x] Interview Qs revised (20+ Q/A in `interview-questions.md`)
