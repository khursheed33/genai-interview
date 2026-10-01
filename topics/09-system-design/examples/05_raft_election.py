"""05_raft_election.py — who's boss? majority, split-votes, higher-term wins.

Run: uv run python topics/09-system-design/examples/05_raft_election.py
"""


def run_term(nodes, ask_order):
    """Each voter grants the FIRST asker of the term; majority (>n/2) wins."""
    voted, tallies = {}, {}
    for cand, voter in ask_order:
        if voter not in voted:
            voted[voter] = cand
            tallies[cand] = tallies.get(cand, 0) + 1
    need = len(nodes) // 2 + 1
    winners = [c for c, v in tallies.items() if v >= need]
    return tallies, winners


nodes = ["a", "b", "c", "d"]  # EVEN cluster: splits happen!

# term 2: a and c race — 2 vs 2, need 3 -> STALEMATE (nobody leads!)
tallies, winners = run_term(
    nodes, [("a", "a"), ("a", "b"), ("c", "c"), ("c", "d"), ("a", "c"), ("c", "a")]
)  # late asks refused!
assert tallies == {"a": 2, "c": 2} and winners == []
print("term 2: 2-2 split, need 3 -> nobody leads (randomized timeouts retry!)")

# term 3: a's timer fires first — sweeps late voters before c starts
tallies, winners = run_term(nodes, [("a", "a"), ("a", "b"), ("a", "c"), ("c", "d")])
assert winners == ["a"], (tallies, winners)
print("term 3: a first ->", tallies, "-> a LEADS (heartbeats hold the lease!)")

# higher term always dethrones: partitioned 'd' returns at term 9, all defer
print("rule: higher term = step down immediately (stale bosses can't scribble!)")
print("OK — majority wins, splits retry with jitter, terms fence the stale!")
