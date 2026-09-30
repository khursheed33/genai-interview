# Exercise 02 — Kill the SCAN (index design)

**Story:** `SELECT * FROM events WHERE tenant_id=? AND kind=?` scans 100k rows. Fix it, prove it.

## Task
In `solution.py`, `fix(conn)` creates the right index on the seeded `events(tenant_id, kind, payload)` table. Seeder + slow query given.

## Acceptance
- `EXPLAIN QUERY PLAN` for the query contains `SEARCH` + `USING INDEX` (no SCAN of events)
- Composite respects leftmost order (tenant first — queries always filter tenant)
