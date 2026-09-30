# 04 — Redis Ops: Disk, Copies & Bouncers (persist/HA/cluster/locks/limits)

## 1. Persistence (RAM is fast, disk forgives)

| Mode | Story | Trade |
|---|---|---|
| RDB (snapshot) | photo every 15 min | compact + fast restart; lose ≤15 min |
| AOF (diary, everysec/always) | every write logged, fsync each second | ≤1s loss; bigger files, slower boot |
| Both (prod!) | photo + diary replay | fast boot + tiny loss |

Size RAM 2× for fork-snapshot (copy-on-write!) + monitor `aof_rewrite` lag.

## 2. HA & scale (copies + captains + shards)

- **Replication**: 1 primary + N async replicas (reads fan out; lag! never read-your-write here). `WAIT` for sync-ack when money matters.
- **Sentinel**: 3+ captains watch, quorum elects new primary on death, clients ask "who's boss?" (VIP/DNS flip!). Split-brain guard: `min-replicas-to-write 1`.
- **Cluster**: 16384 hash slots sharded across primaries (+replicas each); client hashes key→slot→node (`MOVED` redirects!). Multi-key ops must share a **hash tag** (`{user:7}.cart` + `{user:7}.orders` = same slot!).
- **Eviction policies**: `noeviction` (error on full — money data!) vs `allkeys-lru` (cache!) vs `volatile-ttl/lru/lfu/random` (mixed DB!). `maxmemory` set ALWAYS (else OOM-killer picks!).

## 3. Distributed lock (Redlock, done right)

```
token = uuid(); SET lock:pay:7 token NX PX 30000   # ONLY if absent, auto-expire!
... work (extend if long!) ...
release: Lua compare token -> DEL (never delete another's lock after YOUR expiry!)
```

- Fencing: lock + monotonic token passed to DB (`UPDATE … WHERE fence = max`) — stale holder's writes rejected even if lock expired mid-work (THE correctness piece most skip!).
- Single Redis: fine for efficiency (leader election-ish); true Redlock = majority of 5 independent nodes (Martin vs Salvatore debate: clocks + GC pauses — know fencing settles it!).

## 4. Rate limit + sessions on Redis (patterns!)

- Sliding window: `ZADD user:7 {now: now}` + `ZREMRANGEBYSCORE` old + `ZCARD` vs limit (atomic via Lua/pipeline — demo in `../examples/05_lock_limit.py`).
- Sessions: `SETEX sess:abc {json} 1800` + sliding refresh on each hit; logout = `DEL` (instant revoke JWT can't do!).

One-liner: **"RDB+AOF, replicas for reads, Sentinel elects, Cluster slots (hash-tag multi-key!), noeviction for truth / allkeys-lru for cache, locks with token+Lua+fence."**
Redis Stack note: **RediSearch** (query Winters `FT.SEARCH`), **RedisJSON** (path ops), **vector search** (`HNSW` index — baby vector DB for RAG prototypes, topic 18!).
