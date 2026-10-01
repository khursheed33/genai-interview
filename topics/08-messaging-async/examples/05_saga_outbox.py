"""05_saga_outbox.py — relay race with undo legs + ghost-proof publishing.

Run: uv run python topics/08-messaging-async/examples/05_saga_outbox.py
"""

# --- outbox: event written in the SAME fake-TX as the row (no dual-write ghost!) ---
DB, OUTBOX, PUBLISHED, SEEN_IDS = {}, [], [], set()


def create_order_tx(order):
    DB[order["id"]] = order  # row...
    OUTBOX.append(
        {"event_id": f"ev-{order['id']}", "type": "OrderCreated", "order": order}
    )  # ...+event, ONE atomic scratch!


def relay():
    for ev in OUTBOX:  # CDC/Debezium tails the log in prod (no polling!)
        if ev["event_id"] not in SEEN_IDS:  # consumer dedupes by event_id!
            SEEN_IDS.add(ev["event_id"])
            PUBLISHED.append(ev)
    OUTBOX.clear()


create_order_tx({"id": 7, "item": "dosa"})
relay()
relay()  # redelivery!
assert len(PUBLISHED) == 1 and DB[7]["item"] == "dosa"
print("outbox: row+event atomic, relay publishes, consumer dedupes (ghost-free!)")


# --- saga orchestration: conductor commands steps, compensates REVERSED ---
STEPS = [
    ("pay", lambda o: True, lambda o: print("  undo: refund", o)),
    ("stock", lambda o: o != "bad-stock", lambda o: print("  undo: restock", o)),
    ("ship", lambda o: True, lambda o: print("  undo: cancel label", o)),
]


def run_saga(order):
    done = []
    for name, do, undo in STEPS:
        if not do(order):
            for _name, _do, undo_fn in reversed(done):  # undo REVERSED!
                undo_fn(order)
            return f"saga FAILED at {name} (compensated {[n for n, _, _ in done][::-1]})"
        done.append((name, do, undo))
    return "saga DONE: paid+stocked+shipped"


assert run_saga("ok-order") == "saga DONE: paid+stocked+shipped"
failed = run_saga("bad-stock")
assert failed.startswith("saga FAILED at stock") and "pay" in failed
print(failed)
print("OK — choreography for 2 steps, conductor beyond; compensations idempotent + reversed!")
