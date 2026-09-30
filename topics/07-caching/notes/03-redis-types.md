# 03 — Redis Types: Toolbox Tour (string→streams + pub/sub + transactions + Lua)

Redis = data-structure server (RAM speed + optional disk). Pick the TYPE that matches the question:

## 1. Types (one line + command + use — all runnable in `../examples/04_redis_types.py`)

| Type | Commands | Use |
|---|---|---|
| String | `SET/GET/INCR/SET NX PX` | sessions, counters, locks, flags (`INCR` = atomic page views!) |
| Hash | `HSET/HGETALL` | objects (`user:7` fields — fetch one field, not whole JSON!) |
| List | `LPUSH/RPOP/BLMOVE` | queues (reliable: `BRPOPLPUSH` backup list!), timelines |
| Set | `SADD/SISMEMBER/SDIFF` | tags, dedup (`seen_ids`), mutual friends (`SINTER`) |
| Sorted Set | `ZADD/ZRANGE/ZINCRBY` | **leaderboards**, rate-limit windows, delayed jobs (score = run-at!) |
| Bitmap | `SETBIT/GETBIT/BITCOUNT` | daily active users (1 bit/user/day — 12KB per MILLION!) |
| HyperLogLog | `PFADD/PFCOUNT` | unique counts ±0.8% in 12KB (no member list!) |
| Stream | `XADD/XREADGROUP/XACK` | Kafka-lite: consumer groups + ACK + PEL (pending list!) |
| Geo | `GEOADD/GEOSEARCH` | "dosas within 2km" (sorted-set magic underneath!) |

## 2. Pub/Sub (shout, no memory!)

`SUBSCRIBE orders` + `PUBLISH orders {...}` = fire-and-forget broadcast (chat, live scores, cache-invalidate fan-out!). Offline subscriber MISSES messages (that's what **Streams** fix — persistent + groups + ACK!). Pattern-sub (`PSUBSCRIBE shop.*`) for multi-tenant fan-out.

## 3. Transactions + Lua (all-or-nothing, server-side!)

- `MULTI/EXEC` (+ optimistic `WATCH`): queue commands, run together. `WATCH` aborts on touched keys (compare-and-swap for counters!).
- **Lua** (`EVAL`): ship LOGIC to data (atomic check-and-set in ONE round trip!). The lock-release classic:

```lua
-- unlock only if MY token (else I delete someone else's lock!)
if redis.call("GET", KEYS[1]) == ARGV[1] then return redis.call("DEL", KEYS[1]) end return 0
```

One atomic trip instead of GET+DEL race (network gap = stolen lock!). fakeredis can't run Lua (verified!) — demo the token-compare in Python + keep this script for prod.

One-liner: **"Strings count, hashes object, zsets rank, bitmaps/HLL count cheap, streams remember, Lua makes check-and-set atomic."**
