# Exercise 04 — One Smart Cook (async parallel + semaphore)

**Story:** Call 5 LLM prompts. Serial = 5s. Parallel = 1s. But provider allows only 2 at once.

## Task
In `solution.py` implement with `asyncio`:
- `fake_call(name, delay)` — `await asyncio.sleep(delay)`, return `f"{name} done"`
- `run_all(names)` — `asyncio.gather` (unlimited, parallel)
- `run_limited(names, limit=2)` — `asyncio.Semaphore(limit)` guard

## Acceptance
- `run_all(["a","b"])` with delay 0.2 takes < 0.35s (not 0.4s serial)
- `run_limited` returns all 5 results, max concurrency never exceeds limit (track via counter in test)
