# Exercise 03 — Gift Wrap Retry (decorator)

**Story:** Payment gateway hiccups once, succeeds next try. Wrap it so caller just calls `pay()` and gets 3 chances.

## Task
Implement `@retry(times=3)` in `solution.py`:
- Retries on `Exception`, re-raises last error if all fail
- Preserves `__name__` via `functools.wraps`
- Works with any args

## Acceptance
- Flaky fn failing twice then succeeding returns value with `@retry(times=3)`
- Always-failing fn raises after exactly 3 attempts
- `wrapped.__name__` == original name
