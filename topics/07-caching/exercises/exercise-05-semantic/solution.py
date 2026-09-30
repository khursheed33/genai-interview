"""Solution: normalize spelling, match meaning, miss freshness."""

import re


def normalize(q):
    return re.sub(r"\s+", " ", q.strip().lower()).rstrip("?!.,")


def jaccard(a, b):
    sa, sb = set(a.split()), set(b.split())
    return len(sa & sb) / len(sa | sb)


class SemanticCache:
    def __init__(self, threshold=0.5):
        self.threshold, self.store = threshold, {}

    def put(self, q, ans):
        self.store[normalize(q)] = ans

    def ask(self, q):
        nq = normalize(q)
        if nq in self.store:
            return self.store[nq], "exact"
        best, score = None, 0.0
        for k in self.store:
            s = jaccard(nq, k)
            if s > score:
                best, score = k, s
        if score >= self.threshold:
            return self.store[best], f"semantic({score:.2f})"
        return None, "miss"
