# Exercise 04 — Count the Votes (quorum + Raft round)

**Story:** Review the agreement math: quorums for reads/writes, one Raft term.

## Task
In `solution.py`:
- `quorum_ok(n, r, w)` → `r + w > n`
- `run_term(nodes, ask_order)` → `(tallies: dict, winners: list)` — first-ask-per-voter wins a vote; winners need `> n/2`

## Acceptance
- `(3,2,2)` strong, `(3,1,1)` not; 4-node 2-2 split → no winners; sweep → single winner
