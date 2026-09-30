# 02 — Eviction & the Four Horsemen (LRU/LFU/FIFO/TTL + stampede/penetration/avalanche/hotkeys)

## 1. Eviction (full tiffin — whose lunch flies out?)

| Policy | Evicts | Use |
|---|---|---|
| LRU | least-recently-used (recency!) | default for APIs/sessions (yesterday's menu out) |
| LFU | least-frequently-used | celebrity content (viral video stays, one-offs leave) |
| FIFO | oldest inserted | simple queues (order of arrival = fairness) |
| TTL/Random | expired / random sample | Redis `volatile-ttl`/`allkeys-lru` — see note 04 policies! |

- Python: `functools.lru_cache(maxsize=128)` (one-line memo!), `cachetools.TTLCache` (TTL + size). LRU in 10 lines: `OrderedDict` + `move_to_end` + `popitem(last=False)` — exercise-02!

## 2. The four horsemen (name + shield — interview candy!)

| Attack | Story | Shield |
|---|---|---|
| **Stampede / thundering herd** | 1000 reqs miss same expired key → 1000 DB hits → DB dies | **singleflight** (1 fetch, rest wait — `../examples/03_singleflight.py`), probabilistic early refresh, `SET NX` lock-fill |
| **Penetration** | queries for NON-existent ids (`/users/-1`) bypass cache every time | **bloom filter** ("definitely-not-here" in 1KB!) + cache NULLs briefly (`null:1` 60s) |
| **Avalanche** | 1M keys same TTL → mass expiry → DB flood | **jitter TTLs** + warm-up scripts + staggered deploys |
| **Hot keys** | celebrity `user:SRK` on ONE Redis shard melts it | **local L1** (in-process copy 1s!) + read replicas + key splitting (`srk:1…N` + scatter-gather) |

- Invalidation (the hard quote): *"only two hard things: cache invalidation and naming"* — version keys (`menu:v42`), write-delete (not update!), events to purge CDN/app (topic 08 outbox!), short TTL where unsure.

One-liner: **"LRU default, jitter TTLs, singleflight stampedes, bloom penetration, L1 hot keys, version to invalidate."**
