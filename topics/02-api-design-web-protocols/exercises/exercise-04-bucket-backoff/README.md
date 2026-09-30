# Exercise 04 — Bouncer + Patient Knocking (bucket + backoff)

**Story:** Launch day: 10k clients hammer `/orders`. The DB melts. Add a bouncer (token bucket) and teach clients patience (backoff+jitter).

## Task
In `solution.py`:
- `Bucket(rate, burst, clock)` — `allow()` refills by `(now-last)*rate`, capped at `burst`. `clock` is a callable returning seconds (tests inject fake time).
- `backoff(attempt, base=0.5, cap=8.0, rng=random)` — `min(cap, base*2**attempt)` with jitter in `[delay/2, delay]`; honor server `Retry-After` via `wait_for(retry_after, computed)` = max of the two.

## Acceptance
- `Bucket(rate=2, burst=2)`: first two `allow()` true, third false; after +1s, two trues again
- `backoff(0)` within `[0.25, 0.5]`; `backoff(10)` never exceeds `cap`
- `wait_for(retry_after=5, computed=0.5) == 5` (server wins)
