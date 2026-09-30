"""07_consistent_hash_quorum.py — ring reshuffles kindly; quorums overlap.

Run: uv run python topics/06-databases/examples/07_consistent_hash_quorum.py
"""

import hashlib

NODES = ["n1", "n2", "n3"]
VNODES = 100


def ring(nodes):
    r = {}
    for n in nodes:
        for i in range(VNODES):
            r[int(hashlib.md5(f"{n}#{i}".encode()).hexdigest(), 16)] = n
    return dict(sorted(r.items()))


def owner(ring_map, key):
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    for pos, node in ring_map.items():
        if h <= pos:
            return node
    return next(iter(ring_map.values()))


KEYS = [f"user:{i}" for i in range(2000)]
before = {k: owner(ring(NODES), k) for k in KEYS}
after = {k: owner(ring([*NODES, "n4"]), k) for k in KEYS}
moved = sum(1 for k in KEYS if before[k] != after[k])
print(f"adding 4th node moved {moved}/{len(KEYS)} keys ({moved / len(KEYS):.0%})")
assert moved / len(KEYS) < 0.45  # ring: only neighbors' slices move (vs %N: ~75%!)


def quorum_ok(n, r, w):
    return r + w > n  # overlap => fresh read


assert quorum_ok(3, 2, 2) and not quorum_ok(3, 1, 1)
print("R+W>N: (3,2,2) strong, (3,1,1) fast+stale — tune per operation!")
print("OK — consistent hashing minimizes reshuffle; quorums trade freshness for speed")
