"""Solution: counter (ordered, unique) + base62 (short, readable)."""

ALPHA = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(n):
    if n == 0:
        return "0"
    out = ""
    while n:
        n, r = divmod(n, 62)
        out = ALPHA[r] + out
    return out


def decode(s):
    n = 0
    for ch in s:
        n = n * 62 + ALPHA.index(ch)
    return n


class Allocator:
    def __init__(self, start):
        self.n = start

    def next(self):
        self.n += 1
        return self.n
