"""06_redis_streams.py — Kafka-lite with groups on fakeredis (REAL X* commands!).

Run: uv run python topics/08-messaging-async/examples/06_redis_streams.py
"""

import fakeredis

r = fakeredis.FakeStrictRedis()
for i in range(4):
    r.xadd("orders", {"id": str(i), "item": "dosa"})
assert r.xlen("orders") == 4

r.xgroup_create("orders", "kitchen", id="0", mkstream=False)
got = []

# c1 reads 2, acks 1 (crash before 2nd ack -> PENDING!)
msgs = r.xreadgroup("kitchen", "c1", {"orders": ">"}, count=2)
for mid, fields in msgs[0][1]:
    got.append((mid, fields))
    if len(got) == 1:
        r.xack("orders", "kitchen", mid)
pending = r.xpending("orders", "kitchen")
assert pending["pending"] == 1, pending  # unacked = visible + redeliverable!
print("group read 2, acked 1 -> pending:", pending["pending"])

# c2 picks up where the group left off (">"), acks all
more = r.xreadgroup("kitchen", "c2", {"orders": ">"}, count=10)
for mid, _ in more[0][1]:
    r.xack("orders", "kitchen", mid)
assert r.xpending("orders", "kitchen")["pending"] == 1  # c1's orphan still pending
print("c2 drained the rest; orphan stays in PEL till claimed (XCLAIM in prod!)")
print("OK — XADD groups + XACK + PEL: streams remember, pub/sub forgets!")
