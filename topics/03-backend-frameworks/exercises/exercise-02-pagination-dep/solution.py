"""Solution: cap at the gate, slice in the handler."""


def clamp_limit(limit, maximum=100):
    return min(max(int(limit), 1), maximum)


def paginate(items, limit=20, offset=0):
    limit = clamp_limit(limit)
    offset = max(int(offset), 0)
    return {"data": list(items[offset : offset + limit]), "total": len(items)}
