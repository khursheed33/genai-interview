"""05_doc_pipeline.py — folders (embed) vs filing room (reference) + conveyor stages.

Run: uv run python topics/06-databases/examples/05_doc_pipeline.py
"""

# --- embed (read-together, bounded) vs reference (shared/unbounded) ---
order_embedded = {"_id": 7, "items": [{"name": "dosa", "qty": 2}], "status": "paid"}
reviews = {"r1": {"order": 7, "stars": 5}, "r2": {"order": 7, "stars": 4}}  # apart: unbounded!
order_ref = {"_id": 7, "review_ids": ["r1", "r2"]}
assert len(order_embedded["items"]) == 1 and len(order_ref["review_ids"]) == 2
print("embed items (1 fetch) | reference 10k reviews (16MB cap safe)")


# --- aggregation conveyor: $match -> $group -> $sort -> $project ---
DOCS = [
    {"city": "blr", "item": "dosa", "amount": 200},
    {"city": "blr", "item": "idli", "amount": 100},
    {"city": "del", "item": "dosa", "amount": 300},
    {"city": "blr", "item": "dosa", "amount": 150},
]


def match(docs, **cond):
    return [d for d in docs if all(d[k] == v for k, v in cond.items())]


def group_sum(docs, key, field):
    out = {}
    for d in docs:
        out[d[key]] = out.get(d[key], 0) + d[field]
    return [{"_id": k, "total": v} for k, v in out.items()]


def sort_desc(docs, field):
    return sorted(docs, key=lambda d: d[field], reverse=True)


result = sort_desc(group_sum(match(DOCS, item="dosa"), "city", "amount"), "total")
assert result == [{"_id": "blr", "total": 350}, {"_id": "del", "total": 300}], result
print("pipeline (match dosa -> group city -> sort):", result)
print("OK — embed bounded-together, reference shared-huge; pipeline = match/group/sort")
