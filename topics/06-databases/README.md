# 06 - Databases

> Scope: README.md section 6: SQL (joins, CTEs, windows, indexes, ACID, pooling, replication), NoSQL (Mongo/Cassandra/ES), Graph (Neo4j/Cypher), TS/OLAP, CAP/PACELC
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- SQL → `notes/01-sql-core.md` (DDL/DML/DCL/TCL, joins, CTE→window ladder, views, routines)
- Modeling → `notes/02-normalization.md` (1NF→BCNF, denormalize reads w/ named sync)
- Indexes → `notes/03-indexes-plans.md` (B-tree/GIN/partial/covering, EXPLAIN ritual, pgvector note)
- TX → `notes/04-transactions.md` (ACID, isolation ghosts, MVCC, deadlocks, SKIP LOCKED, pooling)
- NoSQL → `notes/05-nosql.md` (5 countries, embed-vs-ref, pipeline, Cassandra keys, ES/BM25)
- Graph → `notes/06-graph.md` (property graph, Cypher, RDF, fraud/recs/GraphRAG)
- OLAP → `notes/07-oltp-olap.md` (counter vs census, columnar, lake/warehouse/lakehouse, JSONB/FTS)
- Theory → `notes/08-distributed-theory.md` (CAP/PACELC/BASE, sharding, quorum, picker, PITR)

## Examples (8 runnable — verified, sqlite stdlib + node)
| File | Covers | Run |
|---|---|---|
| `examples/01_ddl_joins_windows.py` | joins, CTE+RANK, view | `uv run python topics/06-databases/examples/01_ddl_joins_windows.py` |
| `examples/02_normalization.py` | 3NF + read-model copy | same pattern |
| `examples/03_indexes_explain.py` | SCAN 2.9ms→SEARCH 0.2ms, partial idx | same pattern |
| `examples/04_transactions.py` | atomic transfer, 20-thread xfer | same pattern |
| `examples/05_doc_pipeline.py` | embed/ref + match/group/sort | same pattern |
| `examples/06_bm25_search.py` | BM25 scratch + FTS5 agree | same pattern |
| `examples/07_consistent_hash_quorum.py` | ring 27% move, R+W>N | same pattern |
| `examples/08_graph_traversal.js` | recs + fraud ring + FoF | `node .../08_graph_traversal.js` |

## Exercises (5 — `uv run pytest topics/06-databases/exercises -q`, 7 tests)
- `exercise-01-cte-window` — paid-only ranks + grand total
- `exercise-02-index-fix` — SCAN→SEARCH proof
- `exercise-03-transfer` — overdraft atomicity
- `exercise-04-pipeline` — full stage chain
- `exercise-05-bm25-ring` — rank order + kind reshuffle

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
- [x] Notes drafted (8 files, library/register/society stories)
- [x] Examples run (8 files, verified: sqlite + node)
- [x] Exercises done (5 exercises, 7 pytest tests green)
- [x] Interview Qs revised (20+ Q/A in `interview-questions.md`)
