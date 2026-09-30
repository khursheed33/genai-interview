"""02_normalization.py — one truth (3NF) + one fast copy (read model).

Run: uv run python topics/06-databases/examples/02_normalization.py
"""

import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(id));
CREATE TABLE order_items (order_id INTEGER, item TEXT, qty INTEGER);
CREATE TABLE order_summary (order_id INTEGER PRIMARY KEY, customer_name TEXT, n_items INTEGER);
INSERT INTO customers VALUES (1,'asha','999'),(2,'bob','888');
INSERT INTO orders VALUES (101,1),(102,1),(103,2);
INSERT INTO order_items VALUES (101,'dosa',2),(101,'idli',1),(102,'poha',1),(103,'dosa',3);
INSERT INTO order_summary
  SELECT o.id, c.name, SUM(i.qty) FROM orders o
  JOIN customers c ON c.id=o.customer_id JOIN order_items i ON i.order_id=o.id GROUP BY o.id;
""")

# phone lives ONCE: update propagates everywhere by construction
db.execute("UPDATE customers SET phone='997' WHERE id=1")
n_phones = db.execute("SELECT COUNT(DISTINCT phone) FROM customers WHERE name='asha'").fetchone()[0]
assert n_phones == 1
summary = db.execute("SELECT * FROM order_summary ORDER BY order_id").fetchall()
assert summary[0] == (101, "asha", 3), summary
print("summary (denormalized read copy):", summary)
print("OK — normalize writes (no dupes), denormalize reads (pre-joined), name the sync!")
