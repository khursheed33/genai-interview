# 07 — DSA + Big-O (Toy Counting)

## 1. Big-O = "if toys grow 10x, how much slower?"

| O | Story | Example |
|---|---|---|
| O(1) | Take first laddoo | `dict` lookup, `arr[0]` |
| O(log n) | Phone book halves each time | binary search |
| O(n) | Check each Tiffin once | loop, linear search |
| O(n log n) | Best sorting | `sorted()`, merge sort |
| O(n²) | Every kid shakes hands with every kid | nested loops |
| O(2ⁿ) | All dress combinations | brute-force subsets |

Drop constants: O(2n) → O(n). Worst-case matters in interviews. Space too: in-place sort O(1) extra vs copy O(n).

Real world: RAG top-k over 1M vectors brute-force O(n) = slow → HNSW index ≈ O(log n). Choosing `list` scan vs `set` lookup decides p99.

## 2. Data structures = organizers

- **Array/list:** shelf, O(1) index, O(n) insert middle.
- **HashMap (`dict`):** almirah with name labels, O(1) avg. Collisions → chaining. Never iterate assuming order (py3.7+ keeps insert order, but don't rely for logic).
- **Set:** dedup + membership. `seen = set()` for "already visited URL?" in crawler.
- **Stack (LIFO):** plate pile — undo, DFS, parantheses check.
- **Queue (FIFO):** school line — BFS, task queue.
- **Heap (`heapq`):** magic bag that always gives smallest — top-k, merge k sorted feeds. Python is min-heap; max-heap via `-x`.
- **Tree:** family tree — file system, DOM, decision tree. BST: left < root < right. Traversals: inorder (sorted), preorder/postorder.
- **Graph:** friends network — nodes + edges. BFS (shortest hops) vs DFS (explore maze). RAG knowledge graph = graph + LLM.
- **Trie:** auto-complete tree — prefix search.

## 3. Patterns you must type blind

- **Two pointers:** `left=0, right=n-1`, move inward. Ex: valid palindrome, pair sum in sorted, remove duplicates.
- **Sliding window:** fixed/variable window over array/string. Ex: max sum of k, longest substring without repeat, RAG chunk overlap.
- **Binary search:** sorted only; `lo<=hi`, `mid=(lo+hi)//2`. Ex: first bad version, search in rotated.
- **Recursion:** function calls itself with smaller toy. Always base case! Ex: factorial, tree walk, backtracking.
- **DP basics:** recursion + memo ("don't solve same homework twice"). Ex: fib with cache, 0/1 knapsack, longest common subsequence. Start: brute → memo → tabulation.

```python
# sliding window — longest without repeating (like unique seats in a row)
def longest_unique(s):
    seen, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

**One-liners:** "Hashmap for O(1) lookup, heap for top-k, sliding window for substrings, BFS for shortest hops."
