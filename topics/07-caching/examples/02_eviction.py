"""02_eviction.py — full tiffin: who flies out? (LRU/LFU/FIFO/TTL).

Run: uv run python topics/07-caching/examples/02_eviction.py
"""

from collections import Counter, OrderedDict


class LRU:
    def __init__(self, cap):
        self.cap, self.d = cap, OrderedDict()

    def get(self, k):
        if k not in self.d:
            return None
        self.d.move_to_end(k)  # touched = recent!
        return self.d[k]

    def put(self, k, v):
        self.d[k] = v
        self.d.move_to_end(k)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)  # evict least-recent


lru = LRU(2)
lru.put("a", 1)
lru.put("b", 2)
lru.get("a")  # a recent now
lru.put("c", 3)  # b (stale) flies out
assert lru.get("b") is None and lru.get("a") == 1
print("LRU: touched 'a' survives, stale 'b' evicted")


class LFU:
    def __init__(self, cap):
        self.cap, self.d, self.hits = cap, {}, Counter()

    def get(self, k):
        if k not in self.d:
            return None
        self.hits[k] += 1
        return self.d[k]

    def put(self, k, v):
        self.d[k] = v
        self.hits[k] += 0
        if len(self.d) > self.cap:
            victim = min(self.d, key=lambda k: self.hits[k])
            del self.d[victim]
            del self.hits[victim]


lfu = LFU(2)
lfu.put("viral", 1)
lfu.put("once", 2)
lfu.get("viral")
lfu.get("viral")
lfu.put("new", 3)  # 'once' (1 hit) flies, viral stays
assert lfu.get("once") is None and lfu.get("viral") == 1
print("LFU: viral video stays, one-off leaves")


class TTL:
    def __init__(self, clock, default=60):
        self.clock, self.default, self.d = clock, default, {}

    def put(self, k, v, ttl=None):
        self.d[k] = (v, self.clock() + (self.default if ttl is None else ttl))

    def get(self, k):
        hit = self.d.get(k)
        if not hit or hit[1] <= self.clock():
            self.d.pop(k, None)
            return None
        return hit[0]


now = {"t": 0.0}
ttl = TTL(clock=lambda: now["t"], default=60)
ttl.put("sess", "abc")
assert ttl.get("sess") == "abc"
now["t"] += 61
assert ttl.get("sess") is None
print("TTL: fresh hit, expired miss (jitter me in prod ±10%!)")
print("OK — LRU recency, LFU fame, TTL expiry; lru_cache/TTLCache for real code")
