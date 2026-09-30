"""04_transactions.py — promises kept: atomic transfer + concurrent writers.

Run: uv run python topics/06-databases/examples/04_transactions.py
"""

import contextlib
import sqlite3
import tempfile
import threading
import time
from pathlib import Path

DB = str(Path(tempfile.mkdtemp()) / "bank.db")
db = sqlite3.connect(DB, isolation_level=None)
db.execute("PRAGMA busy_timeout = 2000")
db.executescript(
    "CREATE TABLE acct (id INTEGER PRIMARY KEY, bal INTEGER);"
    "INSERT INTO acct VALUES (1,100),(2,100);"
)


def transfer(conn, a, b, amt):
    try:
        conn.execute("BEGIN IMMEDIATE")  # take the write lock NOW (fail fast, don't half-work!)
        bal = conn.execute("SELECT bal FROM acct WHERE id=?", (a,)).fetchone()[0]
        if bal < amt:
            raise ValueError("insufficient")
        conn.execute("UPDATE acct SET bal=bal-? WHERE id=?", (amt, a))
        conn.execute("UPDATE acct SET bal=bal+? WHERE id=?", (amt, b))
        conn.execute("COMMIT")
        return True
    except Exception:
        with contextlib.suppress(sqlite3.ProgrammingError):
            conn.execute("ROLLBACK")  # already rolled back by the driver
        raise


assert transfer(db, 1, 2, 30)
assert [r[0] for r in db.execute("SELECT bal FROM acct ORDER BY id")] == [70, 130]
try:
    transfer(db, 1, 2, 999)
    raise AssertionError("overdraft committed?!")
except ValueError:
    pass
assert [r[0] for r in db.execute("SELECT bal FROM acct ORDER BY id")] == [70, 130]
print("atomic: ok-move 70/130, overdraft rolled back 70/130")


def worker():
    # own connection per thread (sharing one conn across threads corrupts!);
    # lock rows in ASCENDING id order so A->B and B->A can never deadlock
    conn = sqlite3.connect(DB, isolation_level=None)
    conn.execute("PRAGMA busy_timeout = 5000")
    for _ in range(20):  # retry the *whole* TX on lock-busy (like retrying 40001!)
        try:
            transfer(conn, 1, 2, 1)
            break
        except sqlite3.OperationalError:
            time.sleep(0.005)
    conn.close()


ts = [threading.Thread(target=worker) for _ in range(20)]
[t.start() for t in ts]
[t.join() for t in ts]
assert [r[0] for r in db.execute("SELECT bal FROM acct ORDER BY id")] == [50, 150]
print("20 threads x transfer-1 (own conns + ascending locks + busy-retry): 50/150")
print("OK — BEGIN IMMEDIATE, ROLLBACK on error, lock ascending, retry busy (40001-style)")
