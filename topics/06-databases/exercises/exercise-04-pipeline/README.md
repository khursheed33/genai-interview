# Exercise 04 — Conveyor Stages (match/group/sort/project)

**Story:** Analytics wants "top dosa cities" from raw order docs. Build the mini-pipeline.

## Task
In `solution.py` implement stage functions over lists of dicts:
- `match(docs, **cond)` — exact filter; `group_sum(docs, key, field)` → `[{"_id": k, "total": v}]`
- `sort_desc(docs, field)`; `project(docs, *fields)` — keep listed keys only

## Acceptance
- Chain `project(sort_desc(group_sum(match(DOCS, item="dosa"), "city", "amount"), "total"), "_id", "total")` equals `[{"_id": "blr", "total": 350}, {"_id": "del", "total": 300}]`
