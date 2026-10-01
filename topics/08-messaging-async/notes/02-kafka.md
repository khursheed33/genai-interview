# 02 — Kafka: Library Ledger at Scale (partitions/groups/offsets/exactly-once)

## 1. Core (one picture: topic → partitions → offsets)

- **Topic** `orders` split into **partitions** P0…P11 (the parallelism unit!). **Key** (`user_id`) hashed → partition: SAME key → SAME partition → **order guaranteed per key** (different keys: no order promise!).
- **Producer**: `acks=all` (leader + replicas confirm) + `enable.idempotence=true` (sequence numbers kill zombie-duplicates after retries!).
- **Consumer group**: 12 partitions ÷ 4 consumers = 3 each; member dies → **rebalance** (pause + reassign — the stop-the-world tax; static membership + incremental cooperative rebalancing soften it).
- **Offset** = bookmark per (group, partition). Commit AFTER processing (at-least-once!) or BEFORE (at-most-once, may skip!). `__consumer_offsets` stores them; lag = `end − committed` (THE metric!).

## 2. Retention & compaction (forgetting policies!)

- **Delete retention** (`7 days / 100GB`): diary pages burn by age/size (replay window!). **Compaction**: keep LAST value per key forever (`user:7 → latest address` — changelog pattern for restores + stream-table joins!).
- Tombstone (`null` value) deletes on compact. Pick per topic: events → delete; state/changelog → compact.

## 3. Exactly-once (the honest version!)

Kafka EOS = **idempotent producer + transactions** (`read_committed` consumers skip aborted!) across consume→produce (stream processing!). End-to-end (→DB) needs **transactional outbox** (note 05!) or idempotent sinks. Say: *"EOS inside Kafka; effectively-once at edges via idempotency keys."*

## 4. Ops one-liners

More partitions = more parallelism AND more rebalance/file-handle cost (hundreds, not millions!). Replication factor 3, `min.insync.replicas=2` (survive 1 death, writes still ack!). Unclean-leader-election NEVER (trades loss for uptime — refuse!). MirrorMaker for DC replication (active-passive + fencing!).

Runnable ledger (partitions, groups, compaction): `../examples/02_kafka_sim.py`.
