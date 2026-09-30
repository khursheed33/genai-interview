# 08 — Distributed Theory: Impossible Triangles & Quorums (CAP/PACELC/BASE/sharding)

## 1. CAP (partition hits → pick TWO of the rest… precisely: CP or AP)

Network WILL split (undersea cable cut!). Then: **CP** (refuse minority writes — banking ledger) or **AP** (take writes, reconcile later — cart likes). Healthy network? CAP says nothing — that's PACELC's job.

## 2. PACELC (the full sentence)

- **IF Partition → A or C** (same as CAP), **ELSE → Latency or Consistency** (replicate synchronously to 3 DCs = consistent but slow; async = fast but stale reads!). PG sync-replica vs async-replica IS this dial.

## 3. BASE vs ACID (the AP lifestyle)

**Basically Available, Soft state, Eventually consistent**: retries + idempotency (topic 02!) + version vectors/CRDTs + "sorry, merging" UX (carts, feeds, DNS!). ACID where money moves; BASE where availability sells.

## 4. Sharding & replication mechanics (the how)

- **Strategies**: hash (`user_id % N` — rebalance pain!), range (hot celebrity range!), directory/lookup, **consistent hashing** (ring: node joins → steals only neighbors' slices — demo in `../examples/07_consistent_hash_quorum.py`).
- **Topologies**: single-leader (PG: writes leader, async followers + lag!), multi-leader (both accept, conflict resolve — shopping carts!), leaderless/Dynamo (client writes N, quorum decides).
- **Quorum**: `R + W > N` → overlap guarantees fresh read (W=2,R=2,N=3 = strong; W=1 = fast+stale). Tune per operation (reads cheap, writes strict for ledger!).
- **SQL vs NoSQL picker**: relations + money + ad-hoc joins → SQL. 10M writes/s + known key access + global → wide-column/doc. Search/fuzzy → ES. Paths/patterns → graph. Meters → columnar/TS.
- **Polyglot reality**: PG (truth) + Redis (hot) + ES (search) + S3 (blobs) + warehouse (history) — each best-of-breed, synced by CDC/outbox (topic 08!).
- **Backups**: full + WAL/PITR ("rewind to 14:32:07!"), test RESTORES (untested backup = rumor), retention tiers (7d hot, 1y cold, legal holds).

One-liner: **"Partition? CP or AP. Healthy? latency or consistency. Quorum R+W>N for fresh reads; hash-ring to reshard kindly."**
