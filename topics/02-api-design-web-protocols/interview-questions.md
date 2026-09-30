# Interview Questions — API Design & Web Protocols

Say the **bold line** first, then the real-world hook.

## REST & design

- [ ] **[theory]** REST's 6 constraints in 60 seconds?
  - **Client-server, stateless, cacheable, uniform interface, layered, code-on-demand(optional). Stateless + cacheable is why it scales.**
  - Hook: Swiggy order — every request carries token + params; waiter (gateway) hides kitchen (services).
- [ ] **[hands-on]** Fix `GET /getOrder?id=1` and `POST /createOrder`.
  - **Nouns in URI, verbs in methods: `GET /orders/1`, `POST /orders`. Plurals, kebab-case, ≤3 nesting.**
- [ ] **[theory]** Safe vs idempotent? Is DELETE idempotent? PATCH?
  - **Safe = no state change (GET/HEAD/OPTIONS). Idempotent = repeat-safe (PUT/DELETE yes — effect same, status may differ 200→404; POST no; PATCH only for set-value ops).**
  - Hook: retrying LLM POST without Idempotency-Key = double billing.
- [ ] **[theory]** Richardson levels + HATEOAS example?
  - **L0 one-URI RPC → L1 resources → L2 verbs+status → L3 links (`_links: {self, cancel, track}`). Links decouple clients from URL building.**
- [ ] **[scenario]** Design `POST /orders` end-to-end (status, headers, errors, slow kitchen).
  - **Validate → `201 Created` + `Location: /orders/101`; errors as RFC7807 problem+json with `traceId`; slow work → `202 Accepted` + `Location: /jobs/77` + poll/webhook.**

## Status / errors / versioning / pagination

- [ ] **[theory]** `401 vs 403`, `400 vs 422`, `502 vs 503 vs 504`?
  - **401 unknown (login!), 403 known-but-no (VIP room). 400 gibberish, 422 meaningful-but-wrong. 502 upstream exploded, 503 try-later (+Retry-After), 504 upstream too slow.**
- [ ] **[hands-on]** Sketch a good error body.
  - **`type` URI + `title` + `status` + `detail` + `instance` + `traceId`; same shape everywhere; never stacks/PII.**
- [ ] **[theory]** Versioning strategies + rules?
  - **URI `/v1` (visible, common) vs header (clean, invisible) vs query (hack). Additive-only in v1; `Deprecation`+`Sunset` headers; never break shipped clients.**
- [ ] **[hands-on]** Offset vs cursor vs keyset — when each?
  - **Offset (`page/limit`) for admin tables only (slow deep, skips on insert). Cursor/keyset (`after_id`, opaque base64) for feeds — stable + index-fast. Cap `limit`, envelope `{data, pageInfo}`.**
- [ ] **[scenario]** 100 creates in one call? 60-second report?
  - **Bulk `POST /bulk/...` (≤100) → `207 Multi-Status` per-item. Slow job → `202` + `Location` + `Retry-After`, poll `pending→done`; LLM → stream SSE instead.**

## HTTP / headers / cookies / CORS

- [ ] **[theory]** HTTP/1.1 vs 2 vs 3 in 3 lines?
  - **1.1: one request per connection (keep-alive reuses). 2: multiplex many streams on TCP (TCP head-of-line). 3: QUIC/UDP per-stream freedom + 0-RTT, mobile-friendly.**
- [ ] **[theory]** Path vs query vs body vs header — where does the password go?
  - **Path = identity, query = filter/sort/page (logged!), body = payload, headers = metadata. Passwords/tokens in body+TLS or `Authorization` — never query.**
- [ ] **[hands-on]** Name 8 headers and their job.
  - **`Authorization`, `Content-Type/Accept`, `Cache-Control`, `ETag/If-None-Match`, `X-Request-ID` (trace!), `Retry-After`, `CSP`, `HSTS`.**
- [ ] **[theory]** `HttpOnly/Secure/SameSite`? Cookie vs localStorage JWT?
  - **HttpOnly hides from JS (XSS-proof), Secure = HTTPS-only, SameSite gates cross-site (Lax default, None+Secure for widgets + CSRF token). Prefer HttpOnly cookies for sessions.**
- [ ] **[scenario]** "CORS error" on `PATCH` with `Authorization` — checklist?
  - **Browser-only gate! Check: `Allow-Origin` mirrors exact origin (no `*`+credentials), `Allow-Methods` has PATCH, `Allow-Headers` lists Authorization, `OPTIONS` route returns 204. curl works = proof it's browser-side.**

## Styles: GraphQL / gRPC / realtime / webhooks

- [ ] **[theory]** GraphQL N+1 + fix? Federation?
  - **100 orders → 101 queries (1 + per-order items). Fix: DataLoader batch (`WHERE id IN`) + per-request cache. Federation stitches team subgraphs behind one gateway.**
- [ ] **[theory]** gRPC 4 patterns + why HTTP/2? Browser problem?
  - **Unary, server-stream, client-stream, bidi (chat). Needs HTTP/2 multiplexing; browsers need grpc-web proxy; binary needs schema to read.**
- [ ] **[hands-on]** SSE vs WebSockets vs webhooks — pick for: LLM tokens, chat, payment notify.
  - **Tokens → SSE (`text/event-stream`, `data:`+`[DONE]`, auto-reconnect). Chat/games → WebSockets (bidi, `101 Switching`). Payment done → webhooks (HMAC, 200 fast, queue work, idempotency-key, DLQ).**
- [ ] **[hands-on]** Verify a webhook by hand?
  - **`hmac.compare_digest(sign(secret, body), header_sig)`; reject mismatch; process async; dedupe by event id.**
- [ ] **[theory]** REST vs GraphQL vs gRPC vs tRPC in one table?
  - **Public CRUD → REST (cacheable). Exact-field mobile → GraphQL. Internal streams → gRPC. TS monorepo → tRPC (shared types, no schema file).**

## Caching / rate limits / tooling / middleware / resilience

- [ ] **[hands-on]** ETag flow? `no-cache` vs `no-store`?
  - **`ETag` → client `If-None-Match` → `304` empty. `no-cache` = revalidate always; `no-store` = never store (secrets). Version URLs to invalidate.**
- [ ] **[theory]** Token vs leaky vs sliding window? What do you return at the limit?
  - **Token bucket = bursts; leaky = smooth drip; sliding = precise billing. Return `429 + Retry-After + X-RateLimit-Remaining`. Backpressure: 503 + shed/degrade/queue.**
- [ ] **[hands-on]** `curl` the status + time? Debug TLS?
  - **`curl -D - -o /dev/null -w "%{http_code} %{time_total}s"`; `-v` for TLS/headers. HTTPie for humans; Postman envs + Newman in CI.**
- [ ] **[theory]** Gateway vs BFF? Middleware order?
  - **Gateway = auth/limits/cache/routing/analytics at edge. BFF = per-client thin shaper. Middleware order: request-id → auth → logging → validation → handler → error-mapper; auth before billable work.**
- [ ] **[hands-on]** Axios interceptors do what?
  - **Attach token + `X-Request-ID` outgoing; refresh-on-401 + retry-once, map errors to Problem incoming.**
- [ ] **[scenario]** Call a flaky provider: timeouts, retries, breaker, fallback — full answer.
  - **"3s timeout, `Idempotency-Key: <uuid>`, retry 3× (0.5/1/2s+jitter) on 429/5xx honoring `Retry-After`; breaker opens at 5 fails/30s → instant fallback (queued + SMS link); bulkhead isolates pools; poison webhooks to DLQ; `X-Request-ID` logged every hop."**
- [ ] **[theory]** Timeouts (which three)? Bulkhead? DLQ?
  - **Connect/read/overall-deadline; missing timeout = one slow provider freezes all workers. Bulkhead = separate pools per dependency. DLQ = park poison after N retries + alert + replay.**

## Gotchas (say unprompted)

- Passwords in query land in logs; `*` + credentials is an illegal CORS combo.
- Retrying non-idempotent POST without keys double-charges (LLM bills per call!).
- Deep GraphQL nesting needs depth/cost limits; offset pagination breaks live feeds.
- `Retry-After` wins over client math; jitter prevents retry stampedes.

## Self-score (0–5)

- REST design: __ / status+errors+pages: __ / HTTP+headers+CORS: __ / styles+realtime: __ / cache+limits: __ / resilience: __
- Whiteboard: problem+json + cursor walk + breaker transitions + preflight headers? Y/N each.
