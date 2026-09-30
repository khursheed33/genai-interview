"""Solution: BM25 from scratch + md5 ring."""

import hashlib
import math
import re

STOP = {"with", "and", "the"}


def _tok(text):
    return [t for t in re.findall(r"[a-z]+", text.lower()) if t not in STOP]


def bm25_rank(query, docs, k1=1.2, b=0.75):
    index, dlen = {}, {}
    for did, text in docs.items():
        toks = _tok(text)
        dlen[did] = len(toks)
        for t in toks:
            index.setdefault(t, {}).setdefault(did, 0)
            index[t][did] += 1
    N, avgdl, scores = len(docs), sum(dlen.values()) / len(docs), {}
    for t in _tok(query):
        postings = index.get(t, {})
        idf = math.log(1 + (N - len(postings) + 0.5) / (len(postings) + 0.5))
        for did, tf in postings.items():
            denom = tf + k1 * (1 - b + b * dlen[did] / avgdl)
            scores[did] = scores.get(did, 0) + idf * (tf * (k1 + 1) / denom)
    return sorted(scores, key=scores.get, reverse=True)


def _ring(nodes, vnodes):
    r = {}
    for n in nodes:
        for i in range(vnodes):
            r[int(hashlib.md5(f"{n}#{i}".encode()).hexdigest(), 16)] = n
    return dict(sorted(r.items()))


def _owner(ring, key):
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    for pos, node in ring.items():
        if h <= pos:
            return node
    return next(iter(ring.values()))


def moved_fraction(keys, nodes_before, nodes_after, vnodes=50):
    rb, ra = _ring(nodes_before, vnodes), _ring(nodes_after, vnodes)
    moved = sum(1 for k in keys if _owner(rb, k) != _owner(ra, k))
    return moved / len(keys)
