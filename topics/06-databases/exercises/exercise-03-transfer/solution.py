"""Solution: lock now, check, move, seal — or tear everything."""

import contextlib
import sqlite3


def seed():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.executescript(
        "CREATE TABLE acct (id INTEGER PRIMARY KEY, bal INTEGER);"
        "INSERT INTO acct VALUES (1,100),(2,100);"
    )
    return db


def balances(conn):
    return [r[0] for r in conn.execute("SELECT bal FROM acct ORDER BY id")]


def transfer(conn, a, b, amt):
    try:
        conn.execute("BEGIN IMMEDIATE")
        if conn.execute("SELECT bal FROM acct WHERE id=?", (a,)).fetchone()[0] < amt:
            raise ValueError("insufficient")
        conn.execute("UPDATE acct SET bal=bal-? WHERE id=?", (amt, a))
        conn.execute("UPDATE acct SET bal=bal+? WHERE id=?", (amt, b))
        conn.execute("COMMIT")
    except Exception:
        with contextlib.suppress(sqlite3.ProgrammingError):
            conn.execute("ROLLBACK")
        raise
