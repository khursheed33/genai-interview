# 03 — HTTP Deep Dive: Post Office Mechanics

## 1. Versions = bullock cart → metro → teleport

| Version | Transport | Superpower | Kid story |
|---|---|---|---|
| HTTP/1.1 | TCP, 1 request per connection (keep-alive reuses) | simple, universal | One-lane road — head-of-line blocking (slow truck blocks all) |
| HTTP/2 | TCP + binary framing + multiplexing + HPACK + server push | many streams on ONE connection | Multi-lane highway — many cars together (but one accident = all stuck: TCP HOL) |
| HTTP/3 | QUIC over UDP | per-stream independence, 0-RTT, fast mobile handover | Helicopters — one crash doesn't stop others; auto switches during train journey |

- **Keep-alive** (1.1): reuse TCP handshake (saves 1–2 RTTs). **Multiplexing** (2/3): parallel requests, one connection. **HPACK/QPACK**: compress repeated headers.
- Interview: "Why gRPC needs HTTP/2?" → multiplexed bidirectional streams. "Why LLM streaming likes 2/3?" → one long-lived stream, headers compressed.

## 2. Anatomy = envelope + letter

```
POST /orders?priority=high HTTP/1.1        ← start line (method, target, version)
Host: api.shop.com                          ← headers (metadata, : ended by blank line)
Authorization: Bearer abc
Content-Type: application/json

{"items": ["dosa"]}                         ← body
```

Response: `HTTP/1.1 201 Created` + headers (`Location: /orders/101`, `X-Request-ID`) + body. Every `X-Request-ID` you generate at edge and log everywhere = find one user's journey in 5 services.

## 3. Where does each datum ride? (path vs query vs body vs header)

| Seat | Example | Rule |
|---|---|---|
| Path param | `/orders/101` | resource identity (required, hierarchical) |
| Query param | `?status=paid&limit=20` | filtering/sorting/pagination (optional, bookmarkable, logged!) |
| Body | `{"items": [...]}` | creation payload (not logged fully — PII!) |
| Header | `Authorization`, `Idempotency-Key`, `X-Request-ID` | cross-cutting metadata (auth, tracing, negotiation) |

Trap: sending passwords in query (`GET /login?pass=x`) → lands in logs/history. Always body + TLS.

## 4. Content types = lunchbox materials

| Type | When | Note |
|---|---|---|
| `application/json` | 95% APIs | charset utf-8; validate schema (Pydantic) |
| `application/x-www-form-urlencoded` | login forms, OAuth token | flat key=value, URL-encoded |
| `multipart/form-data` | file upload + fields (photo + caption) | boundary-separated; stream, don't buffer 500 MB! |
| `application/octet-stream` | raw binary download | + `Content-Disposition: attachment; filename=bill.pdf` |
| `application/x-ndjson` | streaming JSON lines (logs, LLM batches) | one JSON per line — parse incrementally |
| `text/event-stream` | SSE (LLM token streaming!) | `data: {...}\n\n` chunks |

## 5. Speed tricks: compression + chunked + streaming

- **Compression** (`Content-Encoding: gzip/br`): server shrinks (~70% for JSON), client inflates. Brotli beats gzip for text; never compress images/video (already squeezed).
- **Chunked transfer** (`Transfer-Encoding: chunked`): unknown total size? Send pieces with sizes — live cricket score, LLM tokens.
- **Streaming responses**: SSE/WebSocket/chunked keep ONE connection open and push pieces. For GenAI chat: `text/event-stream` + `data: token` chunks + `data: [DONE]` — user reads while model still writes (TTFT feels instant).

Recap one-liners: **"Path identifies, query filters, body carries, headers whisper." / "Compress text, chunk streams, never passwords in query."**
