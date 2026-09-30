"""Solution: hashmap / sliding window / heap — the 3 must-know patterns."""

import heapq
from collections import Counter


def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], i)
        seen[x] = i
    return None


def longest_unique(s):
    seen, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best


def top_k_freq(items, k):
    return heapq.nlargest(k, Counter(items).items(), key=lambda kv: kv[1])
