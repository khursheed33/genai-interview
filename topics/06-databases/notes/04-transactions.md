# 04 — Transactions: Promises, Ghosts & Traffic Police (ACID → MVCC → deadlocks)

## 1. ACID = promise rigor (money moves need ALL four)

- **Atomicity**: all-or-nothing (`BEGIN; debit; credit; COMMIT` — crash mid-way → `ROLLBACK`, never half-moved).
- **Consistency**: rules hold (`CHECK balance >= 0`, FKs — bad states un-committable).
- **Isolation**: concurrent promises don't see each other's drafts (levels below!).
- **Durability**: committed = survives crash (WAL flushed to disk — that's why `fsync` matters).

## 2. Isolation levels (which ghosts may appear?)

| Level | Dirty read | Non-repeatable | Phantom | PG story |
|---|---|---|---|---|
| Read Committed | ❌ | ✅ possible | ✅ possible | default: each STATEMENT sees fresh snapshot |
| Repeatable Read | ❌ | ❌ | ✅ (PG: ❌!) | TX sees one snapshot; PG also blocks phantoms (SSI-lite) |
| Serializable | ❌ | ❌ | ❌ | true serial order (retry `40001` on conflict!) |

- **Lost update**: both read 100, +50, write 150 (should be 200!) → `SELECT … FOR UPDATE` (row lock) or optimistic `UPDATE … WHERE version = ?` + retry.
- **MVCC**: readers NEVER block writers (each sees a snapshot version; old row versions vacuumed later) — why PG reads scale. Cost: bloat + vacuum.
- **Deadlock**: A locks row1→wants row2, B locks row2→wants row1 → DB kills one (`deadlock_detected`, retry it!). Prevention: lock order (always parent→child, ids ascending!) + short TXs.
- **Locking flavors**: row (`FOR UPDATE`), table, advisory (`pg_advisory_lock` — app-level mutex in DB!), `SKIP LOCKED` (queue pattern: grab next free job without waiting!).

Demo (transfer atomicity + busy-retry + lock ordering): `../examples/04_transactions.py`.
Pooling: PgBouncer (transaction-mode!) + `pool_size` from topic 03 — pool exhaustion looks EXACTLY like DB slowness (check pool wait first!).
