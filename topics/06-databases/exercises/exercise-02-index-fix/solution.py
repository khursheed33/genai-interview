"""Solution: composite (tenant_id, kind) — leftmost serves the actual filter."""

import sqlite3

QUERY = "SELECT * FROM events WHERE tenant_id = 7 AND kind = 'click'"


def seed():
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE TABLE events (id INTEGER PRIMARY KEY, tenant_id INTEGER, kind TEXT, payload TEXT)"
    )
    db.executemany(
        "INSERT INTO events VALUES (?,?,?,?)",
        [(i, i % 50, "click" if i % 3 else "view", "x") for i in range(20_000)],
    )
    db.commit()
    return db


def plan(conn):
    return " ".join(r[3] for r in conn.execute(f"EXPLAIN QUERY PLAN {QUERY}").fetchall())


def fix(conn):
    conn.execute("CREATE INDEX idx_events_tenant_kind ON events (tenant_id, kind)")
