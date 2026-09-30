# 08 — Resilience: Raincoat, Fuse Box & Spare Tiffin

Upstream WILL fail (provider 503, timeout, deploy). Resilience = behave gracefully, retry smartly, never double-charge.

## 1. Timeouts = "wait max 3s, then leave" (ALWAYS set!)

No timeout = one slow provider freezes ALL your workers (threadpool exhaustion → full outage). Set three: **connect** (2s), **read** (5–10s for APIs; 60–120s for LLM streams), **overall deadline** (propagate `Deadline` header through the chain). Client faster than server: return `503` quickly, don't queue forever.

## 2. Retries: exponential backoff + jitter (polite knocking)

Retry ONLY when safe: network errors, `429`, `502/503/504`, timeouts. NEVER blindly retry non-idempotent POST (payment/LLM charge!) without `Idempotency-Key`.

```
attempt waits: 0.5s → 1s → 2s → 4s (+ random jitter ±50%)
```

- Exponential (1,2,4,8) avoids thundering herd; **jitter** (random) stops 1000 clients knocking in sync after an outage. Cap (max 30s) + max attempts (3–5) + overall deadline.
- `Retry-After` header from server WINS over your computation. Idempotency-Key (UUID per logical op, stored 24h with response) makes POST retry-safe: server returns stored response instead of re-charging.

## 3. Circuit breaker = home fuse box (3 states)

```
CLOSED (normal) ──5 failures/30s──→ OPEN (fail fast 30s, no calls!) ──timeout──→ HALF-OPEN (1 probe) ──ok→ CLOSED / fail→ OPEN
```

- OPEN returns fallback instantly (cached menu, "kitchen busy" page) instead of piling timeouts. Probe with 1 request before full traffic.
- **Bulkhead** = ship compartments: separate pools for `/payments` vs `/search` (LLM vs DB threads!) so one flood can't sink all. **Fallback** = spare tiffin: stale cache, default ranking, queue-for-later (`202`). **Graceful degradation**: search without personalization > error page.
- **DLQ** (dead letter queue): poison webhook/queue message retried 5× → park in DLQ + alert, keep pipeline flowing. Inspect, fix, replay.

## 4. Put it together (payment call, the interview answer)

> "Checkout calls gateway with 3s timeout, `Idempotency-Key: <order-uuid>`, retry 3× (0.5/1/2s + jitter) on 429/5xx honoring `Retry-After`. Breaker opens after 5 failures/30s, serves 'queued — pay link by SMS' fallback; bulkhead isolates payment pool; failed webhooks go to DLQ with alert. Every hop logs `X-Request-ID`."

One-liners: **"Timeout everything; retry with backoff+jitter only if idempotent; breaker fails fast; bulkhead isolates; DLQ parks poison."**
Runnable: `../examples/04_rate_limit_retry.py`, `../examples/05_circuit_breaker.py`.
