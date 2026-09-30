"""Solution: token bucket + capped jittered backoff, Retry-After wins."""

import random


class Bucket:
    def __init__(self, rate, burst, clock):
        self.rate, self.burst, self.clock = rate, burst, clock
        self.tokens, self.last = float(burst), clock()

    def allow(self):
        self.tokens = min(self.burst, self.tokens + (self.clock() - self.last) * self.rate)
        self.last = self.clock()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


def backoff(attempt, base=0.5, cap=8.0, rng=random):
    delay = min(cap, base * 2**attempt)
    return delay / 2 + rng.uniform(0, delay / 2)


def wait_for(retry_after, computed):
    if retry_after is None:
        return computed
    return max(float(retry_after), computed)
