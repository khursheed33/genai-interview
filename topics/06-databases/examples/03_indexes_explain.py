"""03_indexes_explain.py — book index vs reading 50k pages (with plans + timings).

Run: uv run python topics/06-databases/examples/03_indexes_explain.py
"""

import sqlite3
import time

db = sqlite3.connect(":memory:")
db.execute(
    "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT, amount INTEGER)"
)
db.executemany(
    "INSERT INTO orders VALUES (?,?,?,?)",
    [(i, i % 500, "paid" if i % 20 else "pending", i % 1000) for i in range(50_000)],
)
db.commit()

Q = "SELECT * FROM orders WHERE user_id = 7 AND status = 'paid'"


def plan():
    return " ".join(r[3] for r in db.execute(f"EXPLAIN QUERY PLAN {Q}").fetchall())


def timed(n=5):
    t0 = time.perf_counter()
    for _ in range(n):
        db.execute(Q).fetchall()
    return (time.perf_counter() - t0) / n * 1000


before_plan, before_ms = plan(), timed()
print(f"before: [{before_plan}] {before_ms:.1f}ms")
assert "SCAN" in before_plan

db.execute("CREATE INDEX idx_orders_user_status ON orders (user_id, status)")
after_plan, after_ms = plan(), timed()
print(f"after:  [{after_plan}] {after_ms:.1f}ms")
assert "SEARCH" in after_plan and "idx_orders_user_status" in after_plan

# partial index: tiny VIP list for the 5% pending slice (on amount — composite can't serve it!)
db.execute("CREATE INDEX idx_pending_amt ON orders (amount) WHERE status = 'pending'")
p = " ".join(
    r[3]
    for r in db.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'pending' AND amount > 900"
    ).fetchall()
)
assert "idx_pending_amt" in p, p
print("partial idx used for hot slice:", "idx_pending_amt" in p)
print(f"OK — SCAN->{after_ms:.1f}ms SEARCH (composite leftmost!); partial for hot 5%")
