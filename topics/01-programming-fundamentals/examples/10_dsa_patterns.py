"""10_dsa_patterns.py — two pointers, sliding window, heap top-k.

Run: uv run python topics/01-programming-fundamentals/examples/10_dsa_patterns.py
"""

import heapq
from collections import Counter


# Two pointers: is palindrome? (front + back walk inward)
def is_pal(s):
    s = "".join(ch.lower() for ch in s if ch.isalnum())
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


print("pal:", is_pal("A man, a plan, a canal: Panama"))  # True


# Sliding window: longest substring without repeat (unique seats in a row)
def longest_unique(s):
    seen, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best


print("longest unique in 'abcabcbb':", longest_unique("abcabcbb"))  # 3
assert longest_unique("abcabcbb") == 3


# Heap: top-2 frequent (magic bag always gives smallest)
orders = ["dosa", "idli", "dosa", "poha", "dosa", "idli"]
top2 = heapq.nlargest(2, Counter(orders).items(), key=lambda kv: kv[1])
print("top2:", top2)  # dosa x3, idli x2
print("OK — two pointers / sliding window / heap cover 80% of interviews")
