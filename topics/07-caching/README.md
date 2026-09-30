# 07 - Caching

> Scope: README.md section 7: strategies, eviction, invalidation/stampede, Redis (types, persistence, Sentinel/Cluster, Redlock), semantic/prompt caching, KV cache
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- Strategies → `notes/01-strategies.md` (aside/through/behind/refresh, delete-not-update, TTL)
- Horsemen → `notes/02-eviction-horsemen.md` (LRU/LFU/FIFO/TTL, stampede/penetration/avalanche/hotkeys)
- Types → `notes/03-redis-types.md` (9 types + pub/sub + MULTI/Lua lock script)
- Ops → `notes/04-redis-ops.md` (RDB/AOF, Sentinel/Cluster/slots, Redlock+fencing, limits/sessions)
- Layers → `notes/05-python-layers.md` (lru_cache/TTLCache, memcached, L1→DB cake)
- LLM → `notes/06-llm-caching.md` (exact/semantic, prompt cache, KV math)

## Examples (8 runnable — verified, fakeredis + threads + node)
| File | Covers | Run |
|---|---|---|
| `examples/01_strategies.py` | aside/through/behind + counters | `uv run python topics/07-caching/examples/01_strategies.py` |
| `examples/02_eviction.py` | LRU/LFU/TTL classes | same pattern |
| `examples/03_singleflight.py` | 20 threads → 1 DB trip | same pattern |
| `examples/04_redis_types.py` | 9 types + pubsub + MULTI (fakeredis) | same pattern |
| `examples/05_lock_limit.py` | token lock + zset sliding window | same pattern |
| `examples/06_python_cache.py` | lru_cache + TTLCache | same pattern |
| `examples/07_semantic_cache.py` | Jaccard semantic + KV math | same pattern |
| `examples/08_http_cache.js` | live 200→304 server | `node .../08_http_cache.js` |

## Exercises (5 — `uv run pytest topics/07-caching/exercises -q`, 9 tests)
- `exercise-01-aside-ttl` — lazy fill, delete-on-write, expiry
- `exercise-02-lru` — O(1) eviction from scratch
- `exercise-03-singleflight` — 1 flight + error-not-cached
- `exercise-04-leaderboard-lock` — zset rank + token lock (fakeredis)
- `exercise-05-semantic` — normalize + threshold + miss-fresh

## Structure
- `README.md` - this checklist entry point
- `notes/` - your condensed notes (add `.md` per sub-topic)
- `examples/` - runnable minimal examples (python/js/sh)
- `exercises/` - practice tasks + solutions
- `interview-questions.md` - Q and A bank

## How to use
1. Read the checklist item in root README.
2. Add notes + code + diagrams here.
3. Do 2-3 exercises and 1 mini-project link in `projects/` if applicable.
4. Self-quiz with interview questions.

## Resources
- Add links as you learn (docs, papers, videos).
- Prefer primary sources: official docs, RFCs, papers.

## Progress
- [x] Notes drafted (6 files, tiffin/horsemen/toolbox stories)
- [x] Examples run (8 files, verified: fakeredis + threads + node)
- [x] Exercises done (5 exercises, 9 pytest tests green)
- [x] Interview Qs revised (20+ Q/A in `interview-questions.md`)
