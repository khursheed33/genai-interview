"""Solution: validate the type, honor the TTL."""

VALID = {"A", "AAAA", "CNAME", "MX", "TXT", "NS", "SRV", "PTR", "SOA"}


def check(rtype):
    return rtype in VALID


class TTLCache:
    def __init__(self, clock):
        self.clock, self.store = clock, {}

    def put(self, name, value, ttl):
        self.store[name] = (value, self.clock() + ttl)

    def get(self, name):
        hit = self.store.get(name)
        if not hit or hit[1] <= self.clock():
            self.store.pop(name, None)
            return None
        return hit[0]
