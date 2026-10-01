# Exercise 01 — Same Key, Same Shelf (partitioning + rebalance)

**Story:** Order events for one user arrive out of order — keys spray randomly. Pin + deal.

## Task
In `solution.py`:
- `partition(key, n)` → stable int in `[0, n)` (hashlib md5)
- `assign(partitions: list, consumers: list)` → dict consumer→partition list (round-robin deal)

## Acceptance
- Same key twice → same partition; all partitions covered exactly once; 4 shelves / 3 clerks = someone holds 2
