"""02_bloom.py — definitely-not-here in 1KB (penetration shield from topic 07!).

Run: uv run python topics/09-system-design/examples/02_bloom.py
"""

import hashlib
import math


class Bloom:
    def __init__(self, n, p=0.01):
        self.m = int(-n * math.log(p) / math.log(2) ** 2)  # bits needed!
        self.k = max(1, round(self.m / n * math.log(2)))  # hash fns!
        self.bits = bytearray((self.m + 7) // 8)

    def _hashes(self, item):
        h1 = int(hashlib.md5(f"{item}:1".encode()).hexdigest(), 16)
        h2 = int(hashlib.md5(f"{item}:2".encode()).hexdigest(), 16)
        return [(h1 + i * h2) % self.m for i in range(self.k)]  # double hashing!

    def add(self, item):
        for h in self._hashes(item):
            self.bits[h // 8] |= 1 << (h % 8)

    def __contains__(self, item):
        return all(self.bits[h // 8] >> (h % 8) & 1 for h in self._hashes(item))


b = Bloom(n=10_000, p=0.01)
print(f"10k URLs: {b.m // 8} bytes, k={b.k} hashes")
assert b.m // 8 < 13_000  # ~12KB!
for u in ["a", "b", "c"]:
    b.add(u)
assert all(u in b for u in ["a", "b", "c"])  # no false NEGATIVES, ever!
fps = sum(1 for i in range(2000) if f"nope-{i}" in b)
print(f"false positives: {fps}/2000 (~1% expected)")
assert fps / 2000 < 0.05
print("OK — 1% FP in 12KB kills DB penetration (pair with cached-NULLs!)")
