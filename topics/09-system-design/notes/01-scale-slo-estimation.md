# 01 — ScaleABC: Counters, Promises & Napkin Math (scale/SLO/estimation)

## 1. Scale directions (which way does the building grow?)

- **Vertical** (bigger server): 4→64 CPU, zero code change — hits a ceiling (and a bill cliff!). **Horizontal** (more servers): infinite-ish, needs statelessness + LB (topic 05!) + shared state (Redis/DB!).
- **Stateless** (any waiter serves you — session in Redis/cookie!) scales by COPY; **stateful** (your waiter remembers — WS rooms, local cache!) needs sticky/sharing (topic 05 sticky = last resort!).

## 2. The four promises (interviewers separate juniors here!)

| Word | Means | Number example |
|---|---|---|
| Latency | ONE request's time (p50/p99!) | p99 checkout 400ms (avg lies — tail kills!) |
| Throughput | requests/sec the system drinks | 10k RPS sustained |
| Availability | % time answering (even degraded!) | 99.9% = 43min/mo DOWN budget |
| Reliability/durability | correct + never-loses-data | 11 nines (S3) = lose 1 file per 10M years |

- **SLI** (measured: p99 <300ms) → **SLO** (promise: 99% of month) → **SLA** (contract + penalty!). **Error budget** = 100% − SLO (0.1% = ship fast till budget burns, then freeze features!). Nines table: 99% (3.6d/yr) → 99.9% (8.7h) → 99.99% (52min) → 99.999% (5min).

## 3. Napkin math (powers of 10 + 5 numbers!)

```
1M DAU × 10 req/day ÷ 86400 ≈ 115 RPS avg (×5 peak = 600!)
1KB × 600 RPS = 600KB/s ≈ 5 Mbps out
1M rows × 1KB = 1GB (×3 replicas = 3GB!)
2.5M sec/mo: 1% of traffic at 1k RPS ≈ 2.5B events/mo (logging $$$!)
```

- Cheat sheet: K=10³ M=10⁶ B=10⁹; 1 char=1B, photo=1MB, movie=1GB; ms (RAM) vs 10ms (SSD) vs 100ms (cross-country RTT!) vs 1s (S3 first byte-ish). Always: **ask** (DAU? read:write? sizes? retention?) → average → ×peak(3–5) → storage ×replicas ×retention → bandwidth → bottlenecks!
- Capacity: one box ≈ 1k–10k simple RPS (measure!) → boxes = peak / per-box × 1.3 headroom. DB: single PG ≈ 5k–20k reads (then replicas/shards — topic 06!).

Runnable estimator: `../examples/01_estimation.py` (QPS/storage/bandwidth + classic answers).
