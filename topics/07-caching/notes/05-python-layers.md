# 05 — Python & Layer Cakes (lru_cache → memcached → L1/L2)

## 1. In-process (L1 — microseconds, per-pod!)

```python
from functools import lru_cache


@lru_cache(maxsize=1024)
def price(item): ...  # same arg = instant; cache_info() shows hits!


import cachetools

ttl = cachetools.TTLCache(maxsize=1000, ttl=60)  # LRU + expiry (sessions, Sylvie menu!)
```

- `lru_cache` keys on ARGS (unhashable dict? `json.dumps` it first!). `typed=True` splits `1` vs `1.0`. **Stampede inside one pod**: 20 threads same miss → wrap with singleflight (topic note 02!). Clear on deploy (`cache_clear()`), size it (unbounded = leak!).

## 2. Memcached (the simple uncle)

Plain string→string sharded pool, LRU, NO persistence/replication/structures (that's the POINT — cache-only!). Multi-threaded, dead simple. Pick when: pure TTL cache at scale, team knows it, no fancy types needed. Else Redis.

## 3. Layer cake (request's journey down the floors)

```
browser (disk/memory, max-age) → CDN edge (shared, versioned!) → LB/app L1 (per-pod copy, 1-5s)
→ Redis L2 (shared, 60s) → DB (+ query cache/buffer pool!) → recompute
```

- Each layer: nearer = faster + smaller + more-duplicated. **Hot keys live at L1** (1s copy kills the celebrity-shard melt!). Invalidation flows DOWN (purge CDN → DEL Redis → bump version).
- HTTP cache (topic 02!): `ETag + max-age` makes browsers/CDNs free Redis. DB cache: PG `shared_buffers` + query cache (ORM `.only()` fewer columns = more fits!).

One-liner: **"L1 per-pod seconds, Redis shared minutes, CDN edge versions; lru_cache + TTLCache locally, memcached for plain, version-purge downward."**
Runnable: `../examples/06_python_cache.py`.
