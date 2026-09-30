# Exercise 03 — One Flight Only (singleflight dedupe)

**Story:** Deploy cleared the cache. 50 threads miss `menu:blr` at once. Prove 1 fetch.

## Task
In `solution.py`, `Flight.get(key, fn)` — first caller runs `fn`, concurrent same-key callers wait and share the result; different keys fly independently; exceptions propagate and DON'T poison the cache.

## Acceptance
- 20 threads same key → `fn` called once, all get value; exception in `fn` → all raisers get it, next call retries (2nd call runs `fn` again)
