# 01 — SQL Core: Library, Joins & Windows (DDL → CTEs → views)

Think of tables as **registers**; SQL as asking the librarian precise questions.

## 1. The four letter-groups (one line each)

- **DDL** (structure): `CREATE/ALTER/DROP TABLE` — build/renovate/demolish shelves.
- **DML** (data): `SELECT/INSERT/UPDATE/DELETE` — daily borrow/return.
- **DCL** (permission): `GRANT/REVOKE` — who may touch which register (app user gets CRUD on 3 tables, nothing else!).
- **TCL** (promises): `COMMIT/ROLLBACK/SAVEPOINT` — "seal it" / "tear it" / "bookmark inside a promise" (more in `04-transactions.md`).

## 2. Joins = combining registers (draw Venn + rows!)

```sql
SELECT u.name, o.item FROM users u
INNER JOIN orders o ON o.user_id = u.id;   -- only matched pairs
LEFT  JOIN orders o ON o.user_id = u.id;   -- ALL users, NULLs where no order
```

- INNER = intersection; LEFT = left all + holes; RIGHT ≈ mirrored (rewrite as LEFT!); FULL OUTER = both + holes (sqlite lacks it — `UNION` two LEFTs); CROSS = every×every (tiny dimensions only!); SELF = employees↔managers same table.
- Trap: `WHERE o.amount > 100` on a LEFT JOIN silently becomes INNER (NULL rows die) — put such filters in `ON`!

## 3. Subquery → CTE → window (readability ladder, same answer)

```sql
WITH paid AS (                                   -- CTE: named temp view, readable + reusable
  SELECT user_id, SUM(amount) AS total FROM orders WHERE status='paid' GROUP BY user_id
)
SELECT u.name, p.total,
  RANK() OVER (ORDER BY p.total DESC) AS rnk,    -- window: rank WITHOUT collapsing rows!
  SUM(p.total) OVER () AS grand_total
FROM users u JOIN paid p ON p.user_id = u.id;
```

- **GROUP BY** collapses (one row per user); **window** (`OVER (PARTITION BY … ORDER BY …)`) computes alongside (running totals, `ROW_NUMBER`, `LAG` for deltas — "yesterday vs today revenue"!). 
- **Views** = saved queries (`CREATE VIEW v_paid AS …`); **materialized** = snapshot refreshed on schedule (dashboards! stale-ok, fast).

## 4. Procedures/triggers/functions (kitchen automation, handle with care)

- **Function** returns a value (`price_with_gst(x)`); **procedure** does steps (`CALL month_end_close()`); **trigger** fires on events (`AFTER INSERT → audit row`). Power + hidden logic = debug hell: keep business rules in code, use triggers ONLY for audit/denormalized counters.

Runnable ladder (DDL→CTE→window→view): `../examples/01_ddl_joins_windows.py`.
