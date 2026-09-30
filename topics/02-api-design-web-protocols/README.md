# 02 - API Design and Web Protocols

> Scope: README.md section 2: REST, GraphQL/SOAP/gRPC/WebSockets/SSE, HTTP deep dive, OpenAPI, middleware/interceptors, resilience patterns
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- REST → `notes/01-rest-foundations.md` (constraints, nouns-vs-verbs, safe/idempotent, RMM/HATEOAS)
- Status+pages → `notes/02-status-errors-versioning.md` (codes, RFC7807, versioning, cursor/keyset, 202+poll)
- HTTP → `notes/03-http-deep-dive.md` (1.1/2/3, anatomy, param seats, content types, streaming)
- Headers → `notes/04-headers-cookies-cors.md` (20 headers, cookie stamps, preflight checklist)
- Styles → `notes/05-other-styles.md` (SOAP, GraphQL N+1/DataLoader, gRPC streams, WS/SSE/webhooks, picker table)
- Cache+limits → `notes/06-caching-rate-limit.md` (ETag→304, token/leaky/sliding, 429+Retry-After)
- Tooling → `notes/07-tooling-middleware.md` (OpenAPI/AsyncAPI, curl, gateways/BFF, onion chain)
- Resilience → `notes/08-resilience.md` (timeouts, backoff+jitter, breaker, bulkhead, DLQ)

## Examples (11 runnable — verified)
| File | Covers | Run |
|---|---|---|
| `examples/01_rest_design.py` | safe/idempotent matrix, naming linter, RMM | `uv run python topics/02-api-design-web-protocols/examples/01_rest_design.py` |
| `examples/02_status_errors_pagination.py` | problem+json, cursor walk 1→10, 202+poll | same pattern |
| `examples/03_caching.py` | ETag→304, Cache-Control | same pattern |
| `examples/04_rate_limit_retry.py` | token bucket, backoff+jitter, idempotency store | same pattern |
| `examples/05_circuit_breaker.py` | closed→open→half-open→closed + fallback | same pattern |
| `examples/06_styles_compare.py` | N+1 (5→1), SOAP envelope, HMAC, style picker | same pattern |
| `examples/07_sse_webhooks_cors.py` | live SSE server+client, preflight check, cookies | same pattern |
| `examples/08_middleware.py` | trace→auth→log onion + timing | same pattern |
| `examples/09_openapi_contract.py` | spec lint + curl gen | same pattern |
| `examples/10_fetch_client.js` | auth+trace interceptor, Retry-After honor | `node .../10_fetch_client.js` |
| `examples/11_sse_parser.js` | SSE tape parser (comments, [DONE]) | `node .../11_sse_parser.js` |

## Exercises (5 — `uv run pytest topics/02-api-design-web-protocols/exercises -q`, 12 tests)
- `exercise-01-orders-api-design` — REST routes + statuses, no verbs
- `exercise-02-cursor-pagination` — opaque cursor walk, no dupes/skips
- `exercise-03-etag-cache` — fingerprint + 304 logic
- `exercise-04-bucket-backoff` — bucket refill + jitter bounds + Retry-After wins
- `exercise-05-breaker-webhook` — breaker states + HMAC sign/verify

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
- [x] Notes drafted (8 files, restaurant/post-office/society-gate stories)
- [x] Examples run (11 files, verified: python + node, live SSE server)
- [x] Exercises done (5 exercises, 12 pytest tests green)
- [x] Interview Qs revised (25+ Q/A in `interview-questions.md`)
