"""02_status_errors_pagination.py — complaint slips + serving 1 lakh dosas.

Run: uv run python topics/02-api-design-web-protocols/examples/02_status_errors_pagination.py
"""

import base64
import json

# --- RFC 7807 problem+json ---
NOT_FOUND = {
    "type": "https://api.shop.com/probs/order-not-found",
    "title": "Order not found",
    "status": 404,
    "detail": "No order 999 in tenant blr",
    "instance": "/orders/999",
    "traceId": "req_abc123",
}
print(json.dumps(NOT_FOUND, indent=None)[:80], "...")
assert NOT_FOUND["status"] == 404 and "traceId" in NOT_FOUND
print("401=unknown person, 403=known but no entry, 202=cooking, 429=slow down")


# --- Cursor pagination (opaque, stable under inserts) ---
def encode_cursor(last_id):
    return base64.urlsafe_b64encode(f"id:{last_id}".encode()).decode()


def decode_cursor(cursor):
    raw = base64.urlsafe_b64decode(cursor.encode()).decode()
    return int(raw.split(":")[1])


ORDERS = [{"id": i} for i in range(1, 11)]  # ids 1..10


def page(after_cursor=None, limit=3):
    start = 0
    if after_cursor:
        last = decode_cursor(after_cursor)
        start = next(i for i, o in enumerate(ORDERS) if o["id"] > last)
    chunk = ORDERS[start : start + limit]
    nxt = encode_cursor(chunk[-1]["id"]) if start + limit < len(ORDERS) else None
    return {"data": chunk, "pageInfo": {"nextCursor": nxt, "hasMore": nxt is not None}}


p1 = page(limit=3)
p2 = page(after_cursor=p1["pageInfo"]["nextCursor"], limit=3)
print("p1 ids:", [o["id"] for o in p1["data"]], "| p2 ids:", [o["id"] for o in p2["data"]])
assert [o["id"] for o in p1["data"]] == [1, 2, 3]
assert [o["id"] for o in p2["data"]] == [4, 5, 6]

# --- Async job pattern: 202 + poll ---
job = {"id": "job_77", "status": "pending", "result": None}
print("POST /index -> 202 Accepted, Location: /jobs/job_77, Retry-After: 5")
job.update(status="done", result="/vectors/idx_9")
assert job["status"] == "done"
print("OK — problem+json errors, cursor pages, 202+poll for slow jobs")
