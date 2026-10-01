# Exercise 03 — Poison Manager (idempotent consumer + DLQ)

**Story:** Retries double-charge; one poison pill stalls the queue. Both fixed here.

## Task
In `solution.py`, `consume(messages, handler, max_tries=3)`:
- Each message `{"id", "body"}`: retry handler up to `max_tries` on `Exception`
- Success twice (same id) → second is `"duplicate"` (no re-run!)
- Exhausted → `dlq` entry `{"id", "tries", "error"}`; return `(done_ids, duplicates, dlq)`

`handler(body)` raises on `"poison"` body, else returns `"ok:<body>"`.

## Acceptance
- `["a","poison","a"]` → done `["a"]`, duplicates `["a"]`, dlq has poison with tries==3; handler ran exactly 1× for "a" success + 3× poison
