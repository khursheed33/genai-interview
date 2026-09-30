"""Solution: 3-state breaker + HMAC webhook guard."""

import hashlib
import hmac


class Breaker:
    def __init__(self, clock, threshold=3, open_secs=10):
        self.clock = clock
        self.threshold, self.open_secs = threshold, open_secs
        self.state, self.fails, self.opened_at = "closed", 0, 0.0

    def call(self, fn, fallback):
        if self.state == "open":
            if self.clock() - self.opened_at >= self.open_secs:
                self.state = "half-open"
            else:
                return fallback("fast-fail")
        try:
            out = fn()
        except Exception as e:
            self.fails += 1
            if self.state == "half-open" or self.fails >= self.threshold:
                self.state, self.opened_at = "open", self.clock()
            return fallback(f"error: {e}")
        self.fails, self.state = 0, "closed"
        return out


def sign(secret: bytes, body: bytes) -> str:
    return hmac.new(secret, body, hashlib.sha256).hexdigest()


def verify(secret: bytes, body: bytes, sig: str) -> bool:
    return hmac.compare_digest(sign(secret, body), sig)
