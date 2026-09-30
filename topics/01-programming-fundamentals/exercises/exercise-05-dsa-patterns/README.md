# Exercise 05 — DSA Mini Pack (two-sum + sliding window + heap)

**Story:** (a) Find two menu prices summing to coupon, (b) longest unique login streak, (c) top-2 dishes.

## Task
In `solution.py`:
- `two_sum(nums, target)` → tuple of indices `(i, j)` in O(n) via hashmap, or `None`
- `longest_unique(s)` → int (sliding window, see notes/07)
- `top_k_freq(items, k)` → list of top-k `(item, count)` via `heapq.nlargest` + `Counter`

## Acceptance
- `two_sum([2,7,11,15], 9) == (0,1)`
- `longest_unique("abcabcbb") == 3`
- `top_k_freq(["dosa","idli","dosa"], 1) == [("dosa", 2)]`
