# 07 — App Defenses: Walls, Alarms & Audits (headers → scanners)

## 1. Security headers (copy-paste starter — in `../examples/07_security_headers.py`)

```
Strict-Transport-Security: max-age=31536000; includeSubDomains   # HTTPS-only year
Content-Security-Policy: default-src 'self'; script-src 'self'; frame-ancestors 'none'; object-src 'none'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

- **CSP** is the XSS killer: even injected `<script src=evil>` won't RUN (not allowlisted). Start `Content-Security-Policy-Report-Only` to find breakage, then enforce. `frame-ancestors 'none'` replaces X-Frame-Options.
- CORS: exact-origin mirror + `Vary: Origin` (cache correctness!), never `*` with credentials (topic 02).

## 2. Input in, output out

- **Validate IN**: Pydantic models (`extra="forbid"`), size caps, allowlists over regex-blocklists. Reject > log > monitor spikes.
- **Encode OUT**: HTML-escape in templates, parameterized SQL, safe serializers (never `pickle` on user data — RCE!). Uploads: type+size+name-randomize (topic 03).

## 3. Abuse armor: limits, WAF, bots

- Per-IP + per-user buckets (topic 02), login-specific stricter (5 tries → CAPTCHA → lockout + alert), DDoS: CDN absorb + edge rules (Cloudflare/AWS Shield), **WAF** (managed OWASP rules + custom: block `169.254` in URL params!), bot checks (TLS fingerprint, behavior) — but keep humans unblocked.

## 4. Scanners in CI (alphabet soup, decoded)

| Scan | Catches | Tool |
|---|---|---|
| SAST | bugs in YOUR code (`exec(user)`) | Semgrep, Bandit, CodeQL |
| SCA | vulns in DEPS (`lodash 4.17.20`) | Dependabot/Renovate + `pip audit`/`npm audit` |
| DAST | running-app holes (missing headers) | OWASP ZAP in staging |
| Secrets | keys in git | gitleaks (already in our CI!) |
| Containers | base-image CVEs | Trivy/Grype on every build |

Fail builds on HIGH/CRITICAL, ticket the rest with SLAs.

## 5. Audit logs (who-did-what — compliance loves these)

`{ts, actor, action, object, result, ip, traceId}` — append-only, tamper-evident (WORM/SIEM), **PII-masked** (see example: `a***@x.com`, card `****1234`). Alert on: privilege changes, bulk exports, auth failures ×N, DLQ growth.

One-liner: **"Headers + validation + WAF outside; SAST/SCA/secrets inside CI; masked audit trail for everything sensitive."**
