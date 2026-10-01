"""Solution: formulas for size, double-hashing for speed."""

import hashlib
import math


def bits(n, p):
    return math.ceil(-n * math.log(p) / math.log(2) ** 2)


def hashes(m, n):
    return max(1, round(m / n * math.log(2)))


class Bloom:
    def __init__(self, n, p=0.01):
        self.m = bits(n, p)
        self.k = hashes(self.m, n)
        self.bits = bytearray((self.m + 7) // 8)

    def _hs(self, item):
        h1 = int(hashlib.md5(f"{item}:1".encode()).hexdigest(), 16)
        h2 = int(hashlib.md5(f"{item}:2".encode()).hexdigest(), 16)
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item):
        for h in self._hs(item):
            self.bits[h // 8] |= 1 << (h % 8)

    def __contains__(self, item):
        return all(self.bits[h // 8] >> (h % 8) & 1 for h in self._hs(item))
