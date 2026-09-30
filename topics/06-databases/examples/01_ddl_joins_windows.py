"""01_ddl_joins_windows.py — librarian's ladder: DDL -> joins -> CTE -> window -> view.

Run: uv run python topics/06-databases/examples/01_ddl_joins_windows.py
"""

import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript("""
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id),
                     item TEXT, amount INTEGER, status TEXT);
INSERT INTO users VALUES (1,'asha','blr'),(2,'bob','del'),(3,'cara','blr');
INSERT INTO orders VALUES (101,1,'dosa',200,'paid'),(102,1,'idli',100,'paid'),
                          (103,2,'poha',150,'pending'),(104,1,'poha',50,'paid');
CREATE VIEW v_paid AS SELECT * FROM orders WHERE status='paid';
""")

inner = db.execute(
    "SELECT u.name, o.item FROM users u INNER JOIN orders o ON o.user_id=u.id"
).fetchall()
assert len(inner) == 4
left = db.execute(
    "SELECT u.name, o.item FROM users u LEFT JOIN orders o ON o.user_id=u.id"
).fetchall()
assert len(left) == 5 and ("cara", None) in left  # cara kept with NULL holes
print("INNER 4 rows | LEFT 5 rows (cara + NULL)")

rows = db.execute("""
WITH paid AS (SELECT user_id, SUM(amount) AS total FROM orders WHERE status='paid' GROUP BY user_id)
SELECT u.name, p.total, RANK() OVER (ORDER BY p.total DESC) AS rnk,
       SUM(p.total) OVER () AS grand
FROM users u JOIN paid p ON p.user_id = u.id ORDER BY rnk""").fetchall()
assert rows[0] == ("asha", 350, 1, 350), rows  # only asha has paid totals; bob pending excluded
print("CTE+window:", rows)
assert db.execute("SELECT COUNT(*) FROM v_paid").fetchone()[0] == 3
print("OK — joins pair registers; CTE names temp work; windows rank without collapsing")
