"""Solution: each stage is a pure function — testable without Mongo."""

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


def project(docs, *fields):
    return [{f: d[f] for f in fields} for d in docs]
