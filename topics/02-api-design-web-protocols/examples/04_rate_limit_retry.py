"""04_rate_limit_retry.py — club bouncer + polite knocking.

Run: uv run python topics/02-api-design-web-protocols/examples/04_rate_limit_retry.py
"""

import random

# --- Token bucket with injectable clock (testable!) ---
NOW = {"t": 0.0}


def now():
    return NOW["t"]


class Bucket:
    def __init__(self, rate, burst):
        self.rate, self.burst = rate, burst
        self.tokens, self.last = float(burst), now()

    def allow(self):
        self.tokens = min(self.burst, self.tokens + (now() - self.last) * self.rate)
        self.last = now()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


b = Bucket(rate=2, burst=2)  # 2 dosas/sec, pocket holds 2
assert [b.allow(), b.allow(), b.allow()] == [True, True, False]  # burst spent
NOW["t"] += 1.0  # 1 sec passes -> 2 tokens refill
assert b.allow() and b.allow()
print("bucket: burst ok, refill ok, 3rd-in-burst rejected (429 + Retry-After)")


# --- Exponential backoff + jitter + Retry-After wins ---
def backoff(attempt, base=0.5, cap=8.0):
    delay = min(cap, base * 2**attempt)
    return delay / 2 + random.uniform(0, delay / 2)  # jitter: half fixed + half random


random.seed(1)
d0 = backoff(0)
assert 0.25 <= d0 <= 0.5, d0
print(f"backoff attempt0 ~ {d0:.2f}s (jittered), attempt3 <= 8s cap")


# --- Idempotency-Key store: pay twice, charge once ---
STORE = {}


def charge(key, amount):
    if key in STORE:
        return STORE[key], False  # replay stored answer, no double charge
    STORE[key] = {"charged": amount}
    return STORE[key], True


r1, fresh1 = charge("ord-101", 500)
r2, fresh2 = charge("ord-101", 500)
assert r1 == r2 and fresh1 and not fresh2
print("OK — 429+Retry-After, backoff+jitter, Idempotency-Key stops double billing")
