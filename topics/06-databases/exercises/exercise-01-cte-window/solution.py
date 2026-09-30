"""Solution: CTE aggregates, window ranks — no collapsing, no N+1 loops."""

import sqlite3


def seed():
    db = sqlite3.connect(":memory:")
    db.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount INTEGER, status TEXT);
    INSERT INTO users VALUES (1,'asha'),(2,'bob'),(3,'cara');
    INSERT INTO orders VALUES (101,1,200,'paid'),(102,1,100,'paid'),
                              (103,2,500,'paid'),(104,2,5,'pending'),(105,3,9,'pending');
    """)
    return db


def top_spenders(conn):
    return conn.execute("""
    WITH paid AS (SELECT user_id, SUM(amount) AS total FROM orders
                  WHERE status='paid' GROUP BY user_id)
    SELECT u.name, p.total, RANK() OVER (ORDER BY p.total DESC) AS rnk,
           SUM(p.total) OVER () AS grand
    FROM users u JOIN paid p ON p.user_id = u.id ORDER BY rnk""").fetchall()
