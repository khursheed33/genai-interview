"""Solution: base64 cursor over last-seen id + keyset slice."""

import base64

ITEMS = [{"id": i} for i in range(1, 11)]


def encode(last_id):
    return base64.urlsafe_b64encode(f"v1:{last_id}".encode()).decode()


def decode(cursor):
    return int(base64.urlsafe_b64decode(cursor.encode()).decode().split(":")[1])


def page(after=None, limit=3):
    start = 0
    if after is not None:
        last = decode(after)
        start = next(i for i, o in enumerate(ITEMS) if o["id"] > last)
    chunk = ITEMS[start : start + limit]
    more = start + limit < len(ITEMS)
    return {
        "data": chunk,
        "pageInfo": {"next": encode(chunk[-1]["id"]) if more else None, "hasMore": more},
    }
