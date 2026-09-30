# 04 — Headers, Cookies, CORS: Name Tags & Society Gates

## 1. Headers cheat-sheet (the 20 that pay salary)

| Header | Direction | Job (one line) |
|---|---|---|
| `Authorization: Bearer <jwt>` | req | who you are (never in URL!) |
| `Content-Type` / `Accept` | both | what I'm sending / what I want back (negotiation: `Accept: application/json`) |
| `Cache-Control: max-age=60, must-revalidate` | res | reuse rules; `no-store` for secrets |
| `ETag: "abc"` / `If-None-Match` | both | fingerprint → `304 Not Modified` (see `06-caching-cdn.md`) |
| `Last-Modified` / `If-Modified-Since` | both | time-based revalidation (weaker than ETag) |
| `Cookie` / `Set-Cookie` | both | session token transport |
| `User-Agent`, `Host`, `Origin`, `Referer` | req | who/where from (analytics, routing, CSRF checks) |
| `X-Forwarded-For/Proto`, `X-Request-ID` | req | real client IP behind proxy; trace ID (generate at edge!) |
| `Retry-After: 30` | res (429/503) | "come back after N sec" — clients MUST honor |
| `Content-Security-Policy` | res | "load scripts ONLY from these sites" (XSS killer) |
| `Strict-Transport-Security` (HSTS) | res | "only HTTPS for next year" |
| `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff` | res | anti-clickjack, anti-MIME-sniff |
| `Transfer-Encoding: chunked` / `Content-Encoding: gzip` | res | streaming pieces / compressed body |

## 2. Cookies = canteen coupon book (with 3 safety stamps)

Server: `Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Lax; Max-Age=3600; Path=/`.

- **HttpOnly** = JS can't touch (XSS thief gets nothing). **Secure** = HTTPS only (no highway robbery). **SameSite** = when to send:
  - `Strict`: only same-site (bank-level; SSO logins may break) 
  - `Lax`: top-level navigation ok, cross-site POST no (sane default)
  - `None`: always (needs `Secure`; for embedded widgets — CSRF risk, pair with tokens!)
- Prefer cookies (HttpOnly) for browser sessions over `localStorage` JWT (XSS-stealable). CSRF then needs `SameSite` + anti-CSRF token.

## 3. CORS = society gate (browser-only rule!)

Browsers block `frontend.com` JS reading `api.shop.com` responses unless API allows. curl/Postman bypass CORS (no gate for them!).

- **Simple** (GET/POST + safe headers): browser sends `Origin`, server replies `Access-Control-Allow-Origin`.
- **Preflight** (PUT/PATCH/DELETE, JSON, custom headers like `Authorization`): browser FIRST sends `OPTIONS` ("may I?"), server must answer:

```
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://frontend.com   (never * with credentials!)
Access-Control-Allow-Methods: GET, POST, PATCH
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 600
```

- Fix checklist for "CORS error": server missing `Allow-Origin`? wildcard `*` + `Access-Control-Allow-Credentials: true` (illegal combo!)? `OPTIONS` route 404? custom header not listed? Interview line: **"CORS is enforced by browsers, not servers — fix server headers, mirror exact origin with credentials."**

Runnable: `../examples/07_sse_webhooks_cors.py` (preflight checker + cookie builder).
