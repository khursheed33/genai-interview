# Exercise 05 — Diary Bank (fold + snapshot + time-travel)

**Story:** Auditors ask "balance last Friday?" and reads replay 1M events. Fold + snapshot + query time.

## Task
In `solution.py`:
- `fold(events)` — `[("credit", n) | ("debit", n)]` → balance
- `with_snapshot(events, every=2)` → `(snapshots: {version: bal}, )` snapshot after every N events (version = count applied)
- `balance_at(events, snapshots, version)` → fold from nearest snapshot ≤ version

## Acceptance
- 4-event fold exact; snapshots at 2,4; `balance_at(3)` uses snapshot@2 + 1 fold; `balance_at(2)` == snapshot
