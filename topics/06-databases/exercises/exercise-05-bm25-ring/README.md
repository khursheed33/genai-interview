# Exercise 05 — Rank + Ring (BM25 order + kind reshuffle)

**Story:** Search returns spam first; adding a shard rehashes 75% keys. Fix both intuitions.

## Task
In `solution.py`:
- `bm25_rank(query, docs: dict[int, str])` → list of doc ids best-first (implement TF×IDF×length-norm from scratch; lowercase + `[^a-z]` tokenize; stopwords `{"with","and","the"}`)
- `moved_fraction(keys, nodes_before, nodes_after, vnodes=50)` → fraction of keys changing owner under consistent hashing (md5 ring)

## Acceptance
- `bm25_rank("dosa", {1: "crispy dosa chutney", 2: "idli poha", 3: "dosa dosa dosa festival menu"}) == [3, 1]`
- Adding 1 node to 3 with 200 keys → moved fraction < 0.45
