# 02 — Status Codes, Errors, Versioning, Pagination

## 1. Status codes = waiter facial expressions (5 families)

| Family | Meaning | Must-know members |
|---|---|---|
| 1xx | "Hold on…" (informational) | `100 Continue`, `101 Switching Protocols` (WebSocket upgrade) |
| 2xx | "Done!" (success) | `200 OK`, `201 Created` (+ `Location` header), `202 Accepted` (async — "order taken, cooking"), `204 No Content` (DELETE ok, empty body) |
| 3xx | "Go there" (redirect) | `301 Moved Permanently`, `302 Found`, `304 Not Modified` (cache hit — with ETag), `307/308` (preserve method) |
| 4xx | "Your mistake" (client) | `400 Bad Request`, `401 Unauthorized` (who are you? login!), `403 Forbidden` (I know you, but no!), `404 Not Found`, `405 Method Not Allowed`, `409 Conflict` (version clash/duplicate), `410 Gone`, `415 Unsupported Media Type`, `422 Unprocessable` (valid JSON, bad semantics), `429 Too Many Requests` (+ `Retry-After`) |
| 5xx | "My mistake" (server) | `500 Internal`, `502 Bad Gateway` (upstream exploded), `503 Service Unavailable` (+ `Retry-After`), `504 Gateway Timeout` |

- `401 vs 403`: **401 = unknown person (show ID); 403 = known person, no entry (VIP room).**
- `400 vs 422`: **400 = gibberish ("asdf" as age); 422 = grammar ok, meaning bad (delivery date in past).**
- GenAI: stream LLM tokens with `200` + SSE; return `429` with `Retry-After` on TPM limits; `502/503` from provider → retry with backoff.

## 2. Error responses = complaint slip (RFC 7807 Problem Details)

Never `{"error": "bad"}`. Send machine-readable + human-readable + traceable:

```json
{ "type": "https://api.shop.com/probs/out-of-stock",
  "title": "Item out of stock", "status": 409,
  "detail": "Dosa batter finished at HSR kitchen",
  "instance": "/orders/101", "traceId": "req_abc123" }
```

Rules: stable `type` URI per error, `traceId`/`X-Request-ID` in every response (grep one request across 5 services!), never leak stack traces or PII, same shape for all endpoints (SDKs love you).

## 3. Versioning = menu editions (pick ONE, stay consistent)

| Strategy | Example | Good | Bad |
|---|---|---|---|
| URI path (common) | `/v1/orders` | visible, cacheable, easy to route | URI pollution |
| Header | `Accept: application/vnd.shop.v2+json` | clean URIs | invisible, hard to test in browser |
| Query | `?version=2` | quick hack | breaks caching, ugly |

Rules: never break v1 (additive only: new optional fields ok, rename/remove = new version), sunset with `Deprecation: true` + `Sunset: Sat, 01 Mar 2026` headers, version the **contract** not every endpoint.

## 4. Pagination = serving 1 lakh dosas (never all at once)

| Method | How | Good | Bad |
|---|---|---|---|
| Offset | `?page=3&limit=20` (`OFFSET 40`) | simple, jump to page | slow deep pages, duplicates/skips on insert, breaks on large offsets |
| Cursor (opaque) | `?cursor=eyJpZDo5OX0&limit=20` (base64 of last seen) | stable under inserts, fast with index | no random jump |
| Keyset | `?after_id=99&limit=20` (`WHERE id > 99`) | fastest, index-friendly | needs sortable unique key, no jump |

- Always: `limit` cap (e.g. max 100), default sort (`sort=-created_at`), envelope: `{data, pageInfo: {nextCursor, hasMore}}`.
- Filtering: `?status=paid&city=blr`; operators namespaced: `?price_gte=100`. Sorting: `?sort=-created,name`. Searching: `?q=dosa` (document it's fuzzy).
- **Partial responses** (save bytes on mobile): `GET /orders/101?fields=id,status,total`. **Bulk**: `POST /bulk/orders` with array (≤100 items), return `207 Multi-Status` per-item results — never all-or-nothing for 100 creates.
- **Long-running** (video render, big RAG index): return `202 Accepted` + `Location: /jobs/77` + `Retry-After: 5`; client polls `GET /jobs/77` (`pending→done` + result link), or better: webhook callback. For LLM: stream tokens (SSE) instead of making client wait 60s.

One-liners: **"401 unknown, 403 known-but-no; 202 + poll for slow jobs; cursor/keyset for feeds, offset only for admin tables."**
Runnable: `../examples/02_status_errors_pagination.py`.
