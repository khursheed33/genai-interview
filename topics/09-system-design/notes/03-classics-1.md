# 03 — Classic Designs I: Short Links, Bouncers & Bells (shortener/rate-limiter/notify)

The interview formula (tattoo it!): **requirements → estimation → API → HLD → deep dive (1–2!) → bottlenecks/trade-offs**. Always clarify FIRST (read-heavy? consistency? scale numbers drive everything!).

## 1. URL shortener (the hello-world!)

```
POST /v1/urls {long} -> 201 {short: "aB3x9Q"}   |   GET /{short} -> 301 + cache
```

- Code: **counter + base62** (no collisions, ordered!) vs **hash + collision-retry** (random, needs check!) — pick counter (ZooKeeper/etcd range allocator per box: 1M IDs in RAM, no single-point write!). 301 (permanent, browsers cache!) vs 302 (analytics count every click!).
- Scale: 100M URLs/mo × 500B = 50GB/mo; reads 10:1 → cache 20% hot (Redis!) + DB sharded by short. Custom aliases (unique index!), expiry (TTL sweeper!), abuse (auth + per-user quota!).
- Runnable mini-service: `../examples/03_url_shortener.py` (FastAPI + base62 + TestClient!).

## 2. Rate limiter (bouncer at scale!)

- Local bucket per box (drift!) vs **central Redis** (exact, RTT!) — hybrid: local fast-path + central sync (cell-based: sticky users per limiter!). Algorithms (topic 02/07!): fixed (boundary spikes!), sliding-log (exact, RAM!), sliding-counter (balanced!), token/leaky (burst vs smooth!).
- Headers: `X-RateLimit-Remaining + Retry-After` (429!). Multi-tier (free 100/min, pro 10k!) + per-endpoint costs (LLM = 100 tokens of budget!). Distributed demo: `../examples/04_limiter_distributed.py`.

## 3. Notification system (bells that never miss!)

```
API -> validate/persist -> queue per CHANNEL (email/sms/push!) -> workers (template+render!)
-> provider (SES/Twilio/FCM!) -> receipts -> retry/DLQ (topic 08!) -> preference center!
```

- Priorities (OTP lane ≠ promo lane — bulkhead!), dedupe (same event twice = one SMS!), quiet hours + frequency caps (spam = uninstalls!), provider failover (Twilio down → Vonage + same idempotency!). Scale: 1B/day = 12k RPS (fan-out ×3 channels!). Templates versioned (render THEN send, never trust stored HTML!).

One-liner: **"Clarify→estimate→API→HLD→1 deep dive→trade-offs; counter+base62 links, central+local limits, channel lanes + dedupe for bells."**
