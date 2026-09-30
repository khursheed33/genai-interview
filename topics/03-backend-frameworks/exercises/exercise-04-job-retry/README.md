# Exercise 04 — Helper Who Doesn't Give Up (retry + idempotency + DLQ)

**Story:** The PDF summarizer flakes on first try and webhooks redeliver. Jobs must survive both.

## Task
In `solution.py` implement (no threads needed — pure logic):
- `run_with_retry(fn, max_tries=3)` → `(result, tries)`; retries on `Exception`; raises last error after `max_tries`
- `process_once(job_id, fn, done: set, dlq: list, max_tries=3)` → `"done"` | `"duplicate"` | `"failed"`; skips if `job_id in done` (adds nothing), on success adds to `done`, on exhaustion appends `(job_id, str(err))` to `dlq`

## Acceptance
- Flaky-twice fn → `("ok", 3)`; always-bad → raises after exactly 3 tries
- Reprocessing a done id → `"duplicate"`, fn NOT called again; poison → `"failed"` + DLQ entry
