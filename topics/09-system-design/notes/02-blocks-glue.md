# 02 — Building Blocks & Distributed Glue (cache/shard/locks/consensus/RPO)

## 1. The standard kit (every design draws these!)

LB (topic 05!) → stateless API → cache (topic 07!) → DB primary + replicas (topic 06!) → queue/workers (topic 08!) → CDN (static!) + object store (blobs!) + search (ES!) + metrics/logs (topic 14!). New pieces below plug INTO this skeleton.

## 2. Partitioning (slice the pizza!)

- **Why**: one box full/slow → split by key (user_id, tenant, geo!). **Hot spots**: celebrity key melts one shard → salt (`srk#1…N`), split writes, L1 cache (topic 07 hot keys!).
- Consistent hashing ring (topic 06/08!) = kind resharding. Range vs hash (hot ranges!) vs directory (lookup table, extra hop!).

## 3. Idempotency + distributed TX (pay-twice protection!)

- Keys on every mutating API (`Idempotency-Key` → stored response replay — topics 02/07!). **2PC** (prepare→commit, coordinator blocks on crash = museum piece, know the phases!). **Saga** (local TXs + compensations — topic 08!) = the working answer.

## 4. Agreement machinery (who's boss?)

- **Leader election**:bully (biggest id wins) / Raft votes (note: demo `../examples/05_raft_election.py`!). **Raft** (majority log replication, terms, heartbeat leases — understandable Paxos!): **Paxos** (proposers/acceptors/learners, single-decree → Multi-Paxos; know the ROLES!). **Gossip** (epidemic state spread: membership/failure detectors — Cassandra/Dynamo style!). **Distributed locks** (Redlock+fencing — topic 07!) for the RARE truly-single job (scheduler leader!).

## 5. Failure math (RPO/RTO + regions!)

- **RPO** (how MUCH data may vanish: 0 = sync replica!) vs **RTO** (how FAST back: 5min DNS flip!). **Active-passive** (cheap, slow flip + grace!) vs **active-active** (fast, conflict resolution + double bill!). Backups + PITR (topic 06!) prove RPO; game-days prove RTO (untested DR = fiction!).
- Failure modes list (say 5!): AZ death, region death, deploy poison (canary+auto-rollback!), dependency cascade (breaker+bulkhead!), data corruption (PITR!), thundering/herd + hot key, cert expiry (monitor!), DNS.

One-liner: **"Slice by key, salt celebrities, idempotency keys everywhere, Raft elects, RPO data-loss vs RTO downtime, active-active costs double."**
