# 05 — Other API Styles: Phone Call, Library, Walkie-Talkie

REST is the restaurant. But sometimes you need a phone call (GraphQL), a legal deed (SOAP), a walkie-talkie (gRPC), or a doorbell (webhooks).

## 1. SOAP = registered legal deed (banks, telecom, govt)

- XML `Envelope > Header + Body`, strict `WSDL` contract + `XSD` types, `Fault` for errors, `WS-Security` (signing/encryption).
- ✅ Strong typing, ACID-ish, tooling generates code. ❌ Verbose XML, rigid, slow to change.
- See one envelope once (in `../examples/06_styles_compare.py` prints it) — interview only asks "when SOAP?" → **regulated legacy where contract rigidity is a feature.**

## 2. GraphQL = librarian who fetches exactly your list

```graphql
query { order(id: 101) { id total items { name price } } }  # ask exactly, get exactly
mutation { cancelOrder(id: 101) { status } }                # writes
subscription { orderUpdates(id: 101) { status } }           # live via WS/SSE
```

- **Resolvers** fetch each field. Trap: **N+1** — 100 orders × 1 query each for items = 101 queries! Fix: **DataLoader** (batch + cache per request: collect 100 item-ids → 1 `WHERE id IN (...)` query).
- **Federation**: many teams own subgraphs (`orders`, `users`), gateway stitches one graph. Schema registry + versioning discipline required.
- ✅ No over/under-fetching, great for mobile. ❌ Caching hard (POST to one endpoint), complexity attacks (deep nested query = DDoS → cost analysis + depth limits), file upload awkward.

## 3. gRPC = walkie-talkie over HTTP/2 (protobuf binary)

```proto
service Route { rpc Chat(stream Msg) returns (stream Msg); }  // bidi streaming!
```

- 4 patterns: **unary** (one ask, one answer), **server-streaming** (one ask, many answers — price ticks), **client-streaming** (many, one — upload chunks), **bidi** (both talk — chat/voice).
- ✅ Binary = tiny + fast, codegen for 10 languages, deadlines/cancellation built-in. ❌ Browser needs proxy (grpc-web), payload unreadable without schema.
- Use: microservice-to-microservice, ML inference, realtime. Real world: Envoy/gateway translates browser REST → internal gRPC.

## 4. Realtime menu: WebSockets vs SSE vs polling vs webhooks

| Style | Direction | How | Use |
|---|---|---|---|
| Short polling | client→server repeatedly | `GET` every 5s | legacy; wasteful |
| Long polling | client waits, server holds | 30s hanging GET | chat before WS |
| **SSE** | server→client only, `text/event-stream` | auto-reconnect, simple | LLM token stream, notifications, scores |
| **WebSockets** | both ways, `ws://` after `101 Switching` | stateful socket | chat, games, collab editing, voice |
| **Webhooks** | server→your URL (event push) | `POST` with HMAC signature | Razorpay "payment done", GitHub push, LLM job completion |

- Webhook safety: verify `HMAC(secret, body) == signature` header, respond `200` fast (queue heavy work), retry with backoff on your 5xx, idempotency-key per event (deliver twice? process once).
- **tRPC**: TypeScript-only RPC — shared types end-to-end, no schema file. **JSON-RPC**: `{"jsonrpc":"2.0","method":"pay","params":{...},"id":1}` over HTTP/WS — simple, batchable.

## 5. The trade-off table (memorize!)

| | REST | GraphQL | gRPC | WS/SSE | Webhooks |
|---|---|---|---|---|---|
| Best for | CRUD, public APIs, caching | mobile/aggregate, exact fields | internal ms, streams, polyglot | live push | event notify |
| Transport | HTTP 1/2/3, JSON | HTTP (WS for subs) | HTTP/2 binary | WS/HTTP stream | HTTP POST |
| Caching | ✅ (URLs) | ❌ hard | ❌ | n/a | n/a |
| Contract | OpenAPI | schema+introspection | protobuf | app-level | signature+docs |

Line to win: **"Public CRUD → REST; exact-field mobile → GraphQL (+DataLoader); internal streams → gRPC; token/notifications → SSE; my-server-needs-event → webhooks; TS monorepo → tRPC."**
Runnable: `../examples/06_styles_compare.py` (N+1 counter, HMAC verify, style picker quiz).
