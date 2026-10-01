"""Solution: overlap for freshness, majority for leadership."""


def quorum_ok(n, r, w):
    return r + w > n


def run_term(nodes, ask_order):
    voted, tallies = {}, {}
    for cand, voter in ask_order:
        if voter not in voted:
            voted[voter] = cand
            tallies[cand] = tallies.get(cand, 0) + 1
    need = len(nodes) // 2 + 1
    return tallies, [c for c, v in tallies.items() if v >= need]
