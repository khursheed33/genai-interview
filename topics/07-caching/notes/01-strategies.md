# 01 — Strategies: Tiffin Habits (aside/through/behind/refresh)

Five ways to keep tiffin (cache) and kitchen (DB) in sync. Same question always: **who fills, who writes, how stale?**

## 1. The five (memorize the table!)

| Strategy | Read path | Write path | Staleness / risk |
|---|---|---|---|
| **Cache-aside** (lazy) | app checks cache → miss → DB → fill cache | app writes DB + **deletes** key | tiny window (delete fails → stale till TTL; fix: TTL + retry delete) |
| **Read-through** | app asks cache; CACHE loads DB on miss | — (reads only pattern) | library hides DB; needs loader fn |
| **Write-through** | like aside | app writes cache AND DB together (slow write, fresh read) | strong-ish; write latency ×2 |
| **Write-behind** (back) | like aside | app writes cache, async flush to DB | FAST writes; crash before flush = LOST (only for losable data: counters, sessions!) |
| **Refresh-ahead** | cache reloads hot keys BEFORE expiry (probabilistic/background) | — | hot keys never miss (leaderboards, LLM system prompts!) |

- Default answer: **cache-aside + TTL** (simple, resilient — DB is truth, cache disposable). High-read static (menu) → read-through/refresh-ahead. Counters/sessions → write-behind with flush workers.
- Delete-during-write (not update!): updating cache with new value races with in-flight reads (old read overwrites new!). **Delete the key, let next read refill** — the one safe sentence.

## 2. TTL (the expiry slip on EVERY key)

No TTL = stale forever + OOM. Rule: **hot+stable = long (menu: 1h), userish = short (profile: 60s), secrets/sessions = shortest + explicit revoke**. Jitter TTLs (±10%) so 10k keys don't expire the same second (mini-avalanche!).

Runnable simulators with hit/miss counters: `../examples/01_strategies.py`.
