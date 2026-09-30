# Interview Questions — Caching

Say the **bold line** first, then the hook.

## Strategies & eviction

- [ ] **[theory]** Aside vs through vs behind vs refresh-ahead — writes for each?
  - **Aside: write DB + DELETE key (never update — races!). Through: cache+DB together (fresh, 2× cost). Behind: cache now, flush later (losable only!). Refresh-ahead: reload hot before expiry.**
- [ ] **[hands-on]** TTL rules + jitter why?
  - **Every key gets TTL (hot-stable long, userish short, secrets shortest). Jitter ±10% stops mass-expiry avalanches.**
- [ ] **[hands-on]** LRU from scratch? `lru_cache` gotchas?
  - **OrderedDict + move_to_end + popitem(front). `lru_cache` keys on args (dump dicts!), `typed`, `maxsize` bounded, `cache_info` proves hits.**
- [ ] **[theory]** Stampede vs penetration vs avalanche vs hot key — shield each?
  - **Singleflight (1 fetch), bloom + cached-NULLs, jittered TTLs + warm-up, L1 replicas/splitting.**

## Redis

- [ ] **[hands-on]** Type per job: counter, object, queue, dedup, leaderboard, DAU, unique count, event log, nearby?
  - **String INCR, hash fields, list, set (SINTER), zset score, bitmap bit, HLL, stream groups, geo search.**
- [ ] **[theory]** Pub/Sub vs Streams? MULTI/EXEC vs Lua?
  - **Pub/Sub shouts (offline misses); Streams remember (groups+ACK+PEL). MULTI batches; Lua runs logic atomically server-side (lock release!).**
- [ ] **[hands-on]** Lock acquire/release done right + fencing?
  - **`SET key token NX PX`; release compares token (Lua) then DEL; fence token into DB writes so stale holders can't scribble.**
- [ ] **[theory]** RDB vs AOF? Sentinel vs Cluster? `noeviction` vs `allkeys-lru`?
  - **Photo + diary together in prod. Sentinel elects (quorum), Cluster slots (hash-tag multi-key!). noeviction for truth, LRU for cache; always `maxmemory`.**
- [ ] **[hands-on]** Sliding-window limiter on zset? Sessions with instant revoke?
  - **ZADD now + ZREMRANGE old + ZCARD ≤ limit (pipeline/Lua). `SETEX sess` + refresh per hit; logout = DEL.**

## Layers & LLM cache

- [ ] **[theory]** Layer cake order + invalidation flow?
  - **Browser → CDN → L1 (per-pod s) → Redis (min) → DB. Purge downward; version keys/CDN files; hot keys duplicated at L1.**
- [ ] **[hands-on]** Exact vs semantic cache + what NEVER to cache?
  - **Exact: sha(normalized+model+temp). Semantic: embed + cosine ≥0.95 (GPTCache/Redis). Never across tenants or fresh data (prices!) — key tenant+date.**
- [ ] **[theory]** Prompt caching rules? KV math for 70B/4k?
  - **Stable prefix first (system→context→user), watch cache_read vs creation. KV ≈ 2×layers×dim×bytes×tokens (~10GB+!) — evict/quantize/page (vLLM).**
- [ ] **[theory]** Memcached vs Redis? RediSearch/JSON/vectors one line?
  - **Memcached = plain sharded TTL (simple!). Stack adds queryable JSON, full-text, and HNSW vectors (RAG prototype DB!).**

## Gotchas (say unprompted)

- Cache update (not delete) on write = stale race; unbounded caches = OOM.
- Lock without token-compare deletes neighbors; no fencing = split-brain writes.
- Same TTL everywhere = avalanche; no tenant in LLM key = cross-user leak.
- `KEYS *` in prod (use SCAN!); reading own writes from async replicas.

## Self-score (0–5)

- Strategies+eviction: __ / redis types: __ / ops+locks: __ / layers+LLM: __
- Whiteboard: aside+TTL + LRU + singleflight + lock Lua? Y/N each.
