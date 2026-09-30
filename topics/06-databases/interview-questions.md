# Interview Questions — Databases

Say the **bold line** first, then the hook.

## SQL core & modeling

- [ ] **[hands-on]** INNER vs LEFT vs FULL vs CROSS vs SELF join + the LEFT-turned-INNER trap?
  - **INNER matched-only; LEFT keeps left + NULL holes; FULL both (UNION in sqlite); CROSS every×every; SELF same table twice (manager). Trap: `WHERE` on right table kills NULL rows — filter in `ON`!**
- [ ] **[theory]** DDL/DML/DCL/TCL one line each? CTE vs subquery vs window vs view?
  - **Structure/data/permission/promise. CTE names temp work; window (`OVER`) computes without collapsing (rank/running totals); view saves query, materialized snapshots it.**
- [ ] **[hands-on]** `GROUP BY` vs window? `ROW_NUMBER` vs `RANK`?
  - **GROUP collapses to one row per group; window keeps rows + adds computation. ROW_NUMBER unique 1,2,3; RANK ties share (1,1,3).**
- [ ] **[theory]** 1NF→2NF→3NF in 30 seconds + when to denormalize?
  - **Atomic cells → whole-key dependence → no transitive chains. Normalize writes (one truth), denormalize reads (pre-joined summary) with a NAMED sync job.**

## Indexes & transactions

- [ ] **[hands-on]** B-tree vs GIN vs partial vs composite-leftmost?
  - **B-tree ranges/sorts; GIN arrays/JSONB/text/vectors; partial indexes hot slices; composite `(a,b)` serves `a` and `a+b`, never `b` alone.**
- [ ] **[hands-on]** Slow query ritual?
  - **`EXPLAIN` → SCAN? add index → SEARCH? measure. Check N+1, `SELECT *`, leading `%like%`, functions on indexed cols, stale stats (`ANALYZE`).**
- [ ] **[theory]** ACID + isolation ghosts + lost update fix?
  - **Atomic/Consistent/Isolated/Durable. Read-committed sees per-statement snapshots (phantoms ok); serializable = true order (retry 40001). Lost update → `SELECT FOR UPDATE` or version-check + retry.**
- [ ] **[hands-on]** Deadlock story + prevention? `SKIP LOCKED` use?
  - **A→row1→row2 vs B→row2→row1 = circular wait; DB kills one (retry!). Prevent: ascending lock order + short TXs. `SKIP LOCKED` = queue grab without waiting.**
- [ ] **[theory]** MVCC in one line? Pool exhaustion vs DB slowness?
  - **Readers see snapshots, never block writers (vacuum cleans old versions). Pool wait looks like DB slowness — check pool first (PgBouncer transaction-mode!).**

## NoSQL / search / graph / OLAP

- [ ] **[hands-on]** Mongo embed vs reference + pipeline stages?
  - **Embed bounded read-together (order+items); reference shared/unbounded (reviews). Pipeline: `$match→$group→$sort→$project`. Shard by co-accessed key (`customer_id`).**
- [ ] **[theory]** Cassandra key design + `R+W>N`?
  - **Partition key spreads, clustering sorts; hot celebrity partition → salt. `R+W>N` overlaps for fresh reads (tune per op: strict writes, cheap reads).**
- [ ] **[hands-on]** Inverted index + BM25 + analyzer mismatch?
  - **Term→docs map; BM25 = TF(saturated) × IDF × length-norm. Same analyzer index+query or zero hits; `text`=search, `keyword`=exact.**
- [ ] **[hands-on]** Cypher for "bought X also bought Y"? Fraud ring pattern?
  - **`MATCH (u)-[:BOUGHT]->(x)<-[:BOUGHT]-(s)-[:BOUGHT]->(y)`. Fraud: shared device/IP across strangers + velocity.**
- [ ] **[theory]** OLTP vs OLAP vs lake vs warehouse vs lakehouse?
  - **Counter (rows, replicas, ms) vs census (columns/Parquet, history). Lake cheap+raw, warehouse governed+fast, lakehouse both (Delta/Iceberg).**
- [ ] **[theory]** CAP vs PACELC vs BASE + sharding kinder how?
  - **Partition→CP/AP; healthy→latency/consistency. BASE = available+eventual (carts/feeds). Consistent-hash ring moves only neighbors' slices; quorum per operation.**

## Gotchas (say unprompted)

- `WHERE` on outer-join NULLs; `SELECT *` on 10M rows; index-everything slows writes.
- Shared connection across threads corrupts (one conn per thread!); `BackgroundTasks` ≠ durable queue.
- Read-your-write on async replicas; untested backup = rumor; vectors need `hnsw/ivfflat` not prayer.

## Self-score (0–5)

- SQL+modeling: __ / indexes+TX: __ / NoSQL+search: __ / graph+OLAP: __ / theory: __
- Whiteboard: window rank + index pick + transfer TX + BM25? Y/N each.
