# 03 — Indexes & Query Plans: Book Index vs Reading Every Page

## 1. Index types (which tool for which question?)

| Index | Story | Use |
|---|---|---|
| B-tree (default) | book index: sorted, range-friendly | `=`, `<`, `>`, `ORDER BY`, prefixes (`LIKE 'dos%'`) |
| Hash | locker numbers (exact only) | `=` lookups (PG hash; no ranges!) |
| Composite `(a, b)` | surname→name index | leftmost rule! `(city, created)` serves `city=` AND `city=+created-range`, NOT `created=` alone |
| Covering `INCLUDE (cols)` | index carries photocopies | query answered WITHOUT touching table (index-only scan!) |
| Partial `WHERE status='paid'` | index only VIP pages | small hot subset (1% unpaid orders!) — tiny + fast |
| GIN / GiST | word→pages (inverted) / maps | arrays, JSONB, full-text (`to_tsvector`), geo, **vectors (ivfflat/hnsw!)** |

## 2. EXPLAIN is the truth (`EXPLAIN QUERY PLAN` / `EXPLAIN ANALYZE`)

```
SCAN orders          <- reading EVERY page (bad at 1M rows!)
SEARCH orders USING INDEX idx_user (user_id=?)   <- index hop (good!)
```

Workflow: slow query → `EXPLAIN` → SCAN on big table? → add/adjust index → re-EXPLAIN (SEARCH?) → measure (`ANALYZE`, buffers, timing). **More indexes ≠ better**: each slows writes + eats RAM — index the WHERE/JOIN/ORDER you actually run (check `pg_stat_statements`!).

## 3. Optimizer greatest hits

- **N+1** (topic 03's twin): loop queries → JOIN/eager-load/batch.
- **SELECT *** + no LIMIT on 10M rows → project columns + keyset pagination (topic 02!).
- `OR` across columns / leading `%like%` / functions on indexed cols (`WHERE YEAR(created)=2024` kills the index — use ranges!) → rewrite or pg_trgm/GIN.
- Stale stats → `ANALYZE`; bloat → `VACUUM`; locks (next note!).

Live demo (50k rows, before/after timings + plans): `../examples/03_indexes_explain.py`.
pgvector note: vectors live in PG via `pgvector` (`ivfflat`/`hnsw` indexes) — our `docker-compose.yml` ships `pgvector/pgvector:pg16`; RAG indexing proper starts in topic 18!
