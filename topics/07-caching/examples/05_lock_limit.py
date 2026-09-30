"""05_lock_limit.py — bouncer badge (lock) + token pocket (rate limit) on fakeredis.

Run: uv run python topics/07-caching/examples/05_lock_limit.py
"""

import time
import uuid

import fakeredis

r = fakeredis.FakeStrictRedis()


def acquire(key, ttl_ms=5000):
    token = uuid.uuid4().hex
    if r.set(key, token, nx=True, px=ttl_ms):  # absent + auto-expire, one trip
        return token
    return None


def release(key, token):
    # Lua in prod (atomic compare-del!); fakeredis: WATCH/MULTI equivalent
    with r.pipeline(transaction=True) as p:
        try:
            p.watch(key)
            if p.get(key) != token.encode():
                p.unwatch()
                return False  # not MY lock (expired + re-taken!) — hands off!
            p.multi()
            p.delete(key)
            p.execute()
            return True
        except Exception:
            return False


t1 = acquire("lock:pay:7")
assert t1 and acquire("lock:pay:7") is None  # second chef waits!
assert release("lock:pay:7", "wrong-token") is False  # stranger's hands off!
assert release("lock:pay:7", t1) is True
print("lock: acquire once, wrong-token safe, right-token frees")


def allow(user, limit=3, window=60, now=None):
    now = time.time() if now is None else now
    key = f"rl:{user}"
    with r.pipeline(transaction=True) as p:
        p.zremrangebyscore(key, 0, now - window)  # forget old sips
        p.zadd(key, {str(now): now})
        p.zcard(key)
        p.expire(key, window)
        results = p.execute()
    return results[2] <= limit


assert [allow("asha", now=1000 + i) for i in range(3)] == [True, True, True]
assert allow("asha", now=1003) is False  # 4th sip in window? bounced (429!)
assert allow("asha", now=1100) is True  # window slid, welcome back
print("limit: 3 sips ok, 4th bounced, next window ok (zset sliding window!)")
print("OK — SET NX PX to take, token-compare to free, zset to count sips")
