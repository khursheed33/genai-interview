"""04_redis_types.py — toolbox tour on fakeredis (same commands as prod!).

Run: uv run python topics/07-caching/examples/04_redis_types.py
"""

import fakeredis

r = fakeredis.FakeStrictRedis()

# string: counters + flags (INCR is atomic!)
r.set("page:home:views", 0)
r.incr("page:home:views", 5)
assert r.get("page:home:views") == b"5"
r.set("lock:x", "tkn", nx=True, px=30000)  # NX + PX = lock acquire, one trip
assert r.get("lock:x") == b"tkn"
print("string: INCR counter + NX/PX lock ok")

# hash: object fields (fetch ONE field, not whole JSON!)
r.hset("user:7", mapping={"name": "asha", "city": "blr"})
assert r.hget("user:7", "city") == b"blr" and r.hlen("user:7") == 2
print("hash: user:7 partial fetch ok")

# list: queue (LPUSH work, BRPOPLPUSH backup in prod!)
r.lpush("q:email", "m1", "m2")
assert r.rpop("q:email") == b"m1" and r.llen("q:email") == 1
print("list: queue push/pop ok")

# set: dedup + mutuals
r.sadd("seen", "u1", "u2", "u1")
r.sadd("a:friends", "x", "y")
r.sadd("b:friends", "y", "z")
assert r.scard("seen") == 2 and r.sinter("a:friends", "b:friends") == {b"y"}
print("set: dedup + SINTER mutuals ok")

# zset: leaderboard + delayed jobs (score = run-at!)
r.zadd("lb", {"asha": 350, "bob": 500, "cara": 100})
assert r.zrevrange("lb", 0, 1) == [b"bob", b"asha"]
r.zadd("jobs", {"j1": 9999999999})
assert r.zrangebyscore("jobs", 0, 9999999998) == []
print("zset: leaderboard top2 + future-job hidden ok")

# bitmap/HLL: cheap counting
r.setbit("dau:2026-09-30", 7, 1)
r.setbit("dau:2026-09-30", 9000, 1)
assert r.bitcount("dau:2026-09-30") == 2  # 2 users in ~1KB!
r.pfadd("uniq", "a", "b", "a")
assert r.pfcount("uniq") == 2  # 12KB, ±0.8% — no member list!
print("bitmap/HLL: 2 users counted in crumbs of RAM")

# geo + streams + pub/sub + transaction
r.geoadd("kitchens", (77.6, 13.0, "blr"))
assert r.geopos("kitchens", "blr")[0][0] > 77.0
mid = r.xadd("orders", {"id": "7"})
assert r.xlen("orders") == 1 and r.xrange("orders")[0][0] == mid
got = []
sub = r.pubsub()
sub.subscribe("news")
sub.get_message()  # swallow subscribe-confirm
r.publish("news", "dosa ready")
msg = sub.get_message(timeout=2)
assert msg and msg["data"] == b"dosa ready"
got.append(msg["data"])
pipe = r.pipeline(transaction=True)
pipe.set("t1", 1)
pipe.incr("t1")
assert pipe.execute() == [True, 2]
print("geo/streams/pubsub/MULTI-EXEC ok | Lua: fakeredis can't (keep script for prod!)")
print("OK — strings count, hashes object, zsets rank, bitmaps/HLL count cheap")
