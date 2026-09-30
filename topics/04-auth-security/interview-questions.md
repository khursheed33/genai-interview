# Interview Questions — Auth, Security & Safety

Say the **bold line** first, then the hook.

## Identity & tokens

- [ ] **[theory]** AuthN vs AuthZ in one breath + session vs JWT trade?
  - **AuthN = who, AuthZ = what. Sessions revoke instantly (stateful); JWT scales (stateless) — so: short access + rotating refresh.**
- [ ] **[hands-on]** Decode a JWT by eye? HS256 vs RS256 — when each?
  - **3×base64url; payload readable, signature sealed. HS256 = one shared secret (single service). RS256 = private signs, many verify via JWKS (microservices).**
- [ ] **[theory]** `exp/aud/iss/jti/alg` — which do you check and why?
  - **All: `exp` (short 5–15m), `aud/iss` (wrong-audience token rejected), `jti` (revocation handle), `alg` whitelisted (`alg:none` attack dies).**
- [ ] **[hands-on]** Refresh rotation + reuse detection?
  - **Each refresh mints a new pair and kills the old jti; reuse of a dead refresh = theft → kill the session family + alert.**
- [ ] **[theory]** OAuth2 grants: auth-code+PKCE vs client-credentials vs device?
  - **Users → auth-code+PKCE (verifier binds code, single-use). Robots → client-credentials. TVs/CLIs → device code. Implicit/password grants are dead.**
- [ ] **[hands-on]** PKCE S256 by hand? Scopes enforced where?
  - **`challenge = base64url(sha256(verifier))`; server compares on redeem. Scopes minimal and enforced server-side per endpoint — UI hiding is not security.**
- [ ] **[theory]** OIDC vs SAML vs LDAP vs Kerberos vs MFA?
  - **OIDC = modern SSO (`id_token`, key users by `sub`). SAML = legacy XML SSO. LDAP = directory phonebook. Kerberos = ticket intranet. MFA = TOTP/WebAuthn second factor; passkeys are phishing-proof.**

## Access control & crypto

- [ ] **[hands-on]** RBAC vs ABAC vs ACL + IDOR guard code?
  - **ACL per object, RBAC badges on routes, ABAC rulebook (role+region+amount+hours). IDOR: owner-or-admin check on the OBJECT every read/write — `GET /orders/7` as Bob → 403.**
- [ ] **[theory]** Hash vs encryption vs encoding + password recipe?
  - **Hash one-way (passwords: argon2/bcrypt + random salt + Vault pepper + constant-time verify). Encryption reversible (AES-GCM bulk, RSA key exchange). Encoding is NOT security (base64).**
- [ ] **[theory]** Envelope encryption + TLS handshake + mTLS in 4 passes?
  - **Data-key per file, KMS wraps keys, master in HSM. TLS: Hello → cert chain verify (CA/expiry/host) → ECDHE session keys → encrypted data (Let's Encrypt 90-day auto-renew). mTLS = both sides show certs (service mesh).**

## OWASP & defenses

- [ ] **[theory]** Top 3 API risks? BOLA fix?
  - **BOLA/IDOR, broken auth, injection. Fix: object-level checks + short rotating tokens + parameterized queries.**
- [ ] **[hands-on]** SQLi vs XSS vs CSRF vs SSRF vs XXE — one lock each?
  - **Placeholders; `html.escape`+HttpOnly+CSP; SameSite+CSRF token (Bearer APIs immune); host allowlist + metadata-IP block; disable DTD (use JSON).**
- [ ] **[hands-on]** Traversal vs clickjacking vs command injection — one lock each?
  - **`resolve()+is_relative_to` + random names; `frame-ancestors 'none'`; argv lists, never `shell=True`.**
- [ ] **[theory]** Headers starter pack? CORS with credentials rule?
  - **HSTS + CSP + `X-Frame-Options: DENY` + `nosniff`. CORS: mirror exact origin + `Vary: Origin`; `*`+credentials is illegal.**
- [ ] **[theory]** SAST vs SCA vs DAST vs secrets vs container scans?
  - **SAST own code (Semgrep), SCA deps (Dependabot/`pip audit`), DAST running app (ZAP), secrets (gitleaks — in our CI!), images (Trivy). Fail on HIGH/CRITICAL.**
- [ ] **[hands-on]** Audit log shape + PII rule?
  - **`{ts, actor, action, object, result, traceId}` append-only; mask before logging (`a***@x.com`, `****1234`). Alert on privilege changes + bulk exports.**

## Privacy & LLM security

- [ ] **[theory]** GDPR deletion vs vector DB? At-rest vs in-transit?
  - **Erase everywhere incl. vectors/backups/caches (the hard part). At-rest AES-GCM/disk, in-transit TLS 1.2+; field-level for SSN.**
- [ ] **[theory]** OWASP LLM Top 10 in 90 seconds?
  - **Injection (untrusted text = DATA + gated tools), disclosure (scrub before index), supply-chain (pin models), poisoning (provenance), output handling (validate model output!), agency (approve side-effects), prompt leak (secret-free system), embedding ACLs (tenant filter at retrieval), hallucination (ground+cite+abstain), budgets (quotas+kill-switch).**
- [ ] **[theory]** Zero trust + SOC2/ISO/HIPAA in one line each?
  - **Zero trust: verify every hop (mTLS/JWT), least-privilege, assume breach. SOC2/ISO/HIPAA = same engineering + evidence (logs, reviews, pen-tests).**

## Gotchas (say unprompted)

- `GET /orders/7` without object check = breach; mass-assignment (`role:admin` in body) needs `extra="forbid"`.
- Long-lived access tokens + no rotation = month-long breach from one laptop.
- Secrets in git/frontend bundle; passwords in query strings; `eval/pickle` on user data (RCE).
- Model output straight to shell/DB = injection via robot.

## Self-score (0–5)

- Identity+tokens: __ / access+crypto: __ / OWASP: __ / defenses: __ / privacy+LLM: __
- Whiteboard: rotation flow + PKCE + IDOR guard + CSP header? Y/N each.
