"""04_limiter_distributed.py — bouncer teamwork: local fast-path + central truth.

Run: uv run python topics/09-system-design/examples/04_limiter_distributed.py
"""

# central truth (Redis in prod!): exact sliding window per key
CENTRAL = {}


def central_allow(key, limit, window, now):
    hits = [t for t in CENTRAL.get(key, []) if t > now - window]
    hits.append(now)
    CENTRAL[key] = hits
    return len(hits) <= limit


# local fast-path per box: token pocket, synced lazily (approximate at edges!)
class LocalBucket:
    def __init__(self, rate, burst):
        self.rate, self.burst, self.tokens, self.last = rate, burst, float(burst), 0.0

    def allow(self, now):
        self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


now = 1000.0
assert [central_allow("free:asha", 3, 60, now + i) for i in range(4)] == [True] * 3 + [False]
print("central: exact 3/min, 4th bounced (429 + Retry-After!)")

b = LocalBucket(rate=1, burst=2)
assert [b.allow(now + i * 0.1) for i in range(3)] == [True, True, False]
print("local: burst 2 ok, 3rd waits (no RTT, approximate at scale!)")

# sticky users per limiter cell (same cell sees full count — hybrid best-of-both!)
cells = {"cell-a": ["asha"], "cell-b": ["bob"]}
assert cells["cell-a"] == ["asha"]
print("OK — central exact, local fast, sticky cells marry them (headers: Remaining + Retry-After!)")
