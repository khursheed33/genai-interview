"""04_semantics_dlq.py — promises (0/1, 1+, effectively-1) + poison + floods.

Run: uv run python topics/08-messaging-async/examples/04_semantics_dlq.py
"""

# --- at-most (ack BEFORE work: crash = lost!) vs at-least (ack AFTER: dupes!) ---
import contextlib

log = []


def process_at_most(msg, crash=False):
    log.append(("ack", msg))  # ack first...
    if crash:
        return "lost!"  # ...boom before work
    log.append(("work", msg))
    return "done"


assert process_at_most("m1", crash=True) == "lost!"
assert ("work", "m1") not in log
print("at-most: crash after ack = silent loss (metrics only!)")


TRIES = {"n": 0}


def process_at_least(msg, store):
    TRIES["n"] += 1
    if TRIES["n"] == 1:
        raise RuntimeError("boom mid-work")  # crash AFTER nothing acked
    if msg["id"] in store:  # idempotency key saves the retry!
        return "duplicate-skipped"
    store.add(msg["id"])
    return "done"


store = set()
with contextlib.suppress(RuntimeError):
    process_at_least({"id": "e7"}, store)  # first attempt crashes mid-work
assert process_at_least({"id": "e7"}, store) == "done"
assert process_at_least({"id": "e7"}, store) == "duplicate-skipped"  # redelivery!
print("at-least + idempotency key = effectively-once (dupes skipped!)")


# --- poison -> DLQ after N tries (main queue flows!) ---
def run_with_dlq(messages, max_tries=3):
    dlq, done = [], []
    for m in messages:
        for _ in range(max_tries):
            if m != "poison":
                done.append(m)
                break
        else:
            dlq.append({"msg": m, "tries": max_tries})  # parked + alert!
    return done, dlq


done, dlq = run_with_dlq(["a", "poison", "b"])
assert done == ["a", "b"] and dlq == [{"msg": "poison", "tries": 3}]
print("DLQ: poison parked with headers, good mail flowed")


# --- backpressure: block vs drop-oldest vs drop-newest (bounded!) ---
def push(q, item, cap, policy):
    if len(q) < cap:
        q.append(item)
        return "kept"
    if policy == "block":
        return "wait (slow producer!)"
    if policy == "drop-oldest":
        q.pop(0)
        q.append(item)
        return "dropped-oldest"
    return "dropped-newest"


qq = [1, 2]
assert push(qq, 3, 2, "drop-oldest") == "dropped-oldest" and qq == [2, 3]
assert push([1, 2], 3, 2, "block") == "wait (slow producer!)"
print("OK — ack-after + idempotency; poison to DLQ; buffers BOUNDED with a policy!")
