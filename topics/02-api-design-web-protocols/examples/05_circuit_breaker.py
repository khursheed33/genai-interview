"""05_circuit_breaker.py — home fuse box (closed/open/half-open).

Run: uv run python topics/02-api-design-web-protocols/examples/05_circuit_breaker.py
"""


class Clock:
    def __init__(self):
        self.t = 0.0

    def advance(self, s):
        self.t += s


class Breaker:
    def __init__(self, clock, fail_threshold=3, open_secs=10):
        self.clock = clock
        self.th, self.open_secs = fail_threshold, open_secs
        self.state, self.fails, self.opened_at = "closed", 0, 0.0

    def call(self, fn, fallback):
        if self.state == "open":
            if self.clock.t - self.opened_at >= self.open_secs:
                self.state = "half-open"  # one probe allowed
            else:
                return fallback("fast-fail")  # fail fast, no pile-up!
        try:
            out = fn()
        except Exception as e:
            self.fails += 1
            if self.state == "half-open" or self.fails >= self.th:
                self.state, self.opened_at = "open", self.clock.t
            return fallback(f"error: {e}")
        self.fails, self.state = 0, "closed"
        return out


clock = Clock()
br = Breaker(clock, fail_threshold=3, open_secs=10)


def boom():
    raise RuntimeError("gateway down")


def fb(reason):
    return f"FALLBACK queued ({reason})"


for _ in range(3):
    print(br.call(boom, fb), "| state:", br.state)
assert br.state == "open"
print(br.call(boom, fb), "| still open -> instant fallback, provider gets rest")
clock.advance(11)  # cool down; next call is the probe
print(br.call(lambda: "recovered!", fb), "| state:", br.state)
assert br.state == "closed"
print("OK — fail fast when open, single probe, fallback = spare tiffin")
