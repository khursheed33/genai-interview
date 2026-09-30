"""03_singleflight.py — 1000 hungry kids, ONE trip to the kitchen.

Run: uv run python topics/07-caching/examples/03_singleflight.py
20 threads miss the same key: naive = 20 DB trips, singleflight = 1.
"""

import threading
import time

FETCHES = {"n": 0}


def slow_db(k):
    time.sleep(0.05)
    FETCHES["n"] += 1
    return f"menu-for-{k}"


# naive: everyone fetches
def naive(keys):
    out, threads = {}, []

    def one(k):
        out[k] = slow_db(k)

    for k in keys:
        t = threading.Thread(target=one, args=(k,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return out


FETCHES["n"] = 0
naive(["blr"] * 20)
print("naive DB trips:", FETCHES["n"])
assert FETCHES["n"] == 20


# singleflight: first flies, rest wait on the SAME flight
class Flight:
    def __init__(self):
        self.lock = threading.Lock()
        self.inflight = {}

    def get(self, k, fn):
        with self.lock:
            if k in self.inflight:
                ev = self.inflight[k]
                waiter = True
            else:
                ev = threading.Event()
                self.inflight[k] = ev
                waiter = False
        if waiter:
            ev.wait()
            return self.inflight.pop(k, None) or CACHE[k]
        try:
            v = fn(k)
            CACHE[k] = v
            return v
        finally:
            with self.lock:
                self.inflight.pop(k, None)
            ev.set()


CACHE, flight = {}, Flight()
FETCHES["n"] = 0
out, threads = {}, []


def one_sf(k):
    out[k] = flight.get(k, slow_db)


ts = [threading.Thread(target=one_sf, args=("blr",)) for _ in range(20)]
[t.start() for t in ts]
[t.join() for t in ts]
print("singleflight DB trips:", FETCHES["n"])
assert FETCHES["n"] == 1 and out["blr"] == "menu-for-blr"
print("OK — stampede shield: dedupe in-flight misses (Go has it stdlib; py hand-rolls!)")
