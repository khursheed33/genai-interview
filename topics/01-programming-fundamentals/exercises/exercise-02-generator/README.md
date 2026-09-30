# Exercise 02 — Factory Conveyor (generator for big logs)

**Story:** A 10 GB Swiggy log file. `readlines()` tries to lift the whole bucket (OOM). Build a tap.

## Task
In `solution.py` implement:
- `line_stream(n)` — `yield f"order-{i}"` for `i in range(n)` (lazy, not a list)
- `active_orders(lines)` — generator that yields only lines not starting with `"CANCELLED"`

## Acceptance
- `line_stream` returns a generator (has `__next__`), not a list
- `list(active_orders(["order-1", "CANCELLED-2", "order-3"])) == ["order-1", "order-3"]`
- Memory: generator for 1M items uses < 1 KB shallow (`sys.getsizeof < 1000`)
