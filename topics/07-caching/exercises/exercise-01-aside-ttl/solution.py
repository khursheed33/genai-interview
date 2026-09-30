"""Solution: lazy fill, delete-on-write, deadline per key."""


class AsideCache:
    def __init__(self, db: dict, clock):
        self.db, self.clock, self.store = db, clock, {}
        self.hits, self.misses = 0, 0

    def get(self, k, ttl=60):
        hit = self.store.get(k)
        if hit and hit[1] > self.clock():
            self.hits += 1
            return hit[0]
        self.misses += 1
        v = self.db[k]
        self.store[k] = (v, self.clock() + ttl)
        return v

    def set(self, k, v):
        self.db[k] = v
        self.store.pop(k, None)
