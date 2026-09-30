# 06 — Caching & Rate Control: Tiffin Memory + Token Bouncer

## 1. HTTP caching = "same dosa as last time?"

Two validators, ETag wins over time:

```
Client:  GET /menu ──────────────────→ Server: 200 + ETag: "v42" + Cache-Control: max-age=60
Client (60s later): GET /menu + If-None-Match: "v42" → Server: 304 Not Modified (empty body!)
```

- **ETag** = fingerprint (`hash(body+version)`). Strong (`"v42"`) vs weak (`W/"v42"` — semantically same). Client sends `If-None-Match`; match → `304`, save bytes.
- **Last-Modified / If-Modified-Since** = wall clock; 1-second resolution, clock-skew issues. Use ETag for APIs, LM for static files.
- **Cache-Control directives**: `max-age=60` (fresh 60s), `no-cache` (revalidate every time — misleading name!), `no-store` (never store — OTPs, personal data), `must-revalidate`, `private` (per-user, not CDN) vs `public`, `stale-while-revalidate=30` (serve stale, refresh behind — feels instant).
- Invalidation (the hard part!): versioned URLs (`/app.v42.js`), short TTL for dynamic, purge CDN API on deploy, `POST /orders` invalidates `GET /orders` (write-through in app cache).

## 2. Rate limiting = club bouncer with token pocket

| Algorithm | Story | Best for |
|---|---|---|
| Token bucket | Pocket refills 10 tokens/sec; each request takes 1; burst allowed till pocket empty | APIs with bursts (LLM: 60 req/min + burst 10) |
| Leaky bucket | Fixed drip out (smooth); queue overflows drop | smooth upstream (webhooks to legacy) |
| Fixed window | "100 per minute" counter resets at :00 | simple; stampede at boundary |
| Sliding window log/counter | Weighted overlap — no boundary spike | precise billing tiers |

- Respond `429 + Retry-After: 12 + X-RateLimit-Remaining: 0`. Client MUST back off (see `08-resilience.md`).
- **Throttling** (slow down: delay) vs **rate limiting** (reject 429) vs **quota** (monthly units: "10k images/mo") vs **backpressure** (server says "I'm full": 503 + shed load, queue, or degrade — serve cached/low-res).
- Where: edge (Cloudflare/AWS WAF), gateway (Kong/Apigee per-key), service (per-user bucket in Redis: `INCR` + `EXPIRE` — atomic Lua for exactness).
- GenAI: separate limits per model (GPT-4o TPM vs embeddings RPM), per-tenant buckets (noisy neighbor!), queue + `202 Accepted` when over — never melt the GPUs.

One-liners: **"ETag→304 saves bytes; version URLs to invalidate." / "Token bucket for bursts, sliding window for billing, 429+Retry-After always."**
Runnable: `../examples/03_caching.py`, `../examples/04_rate_limit_retry.py`.
