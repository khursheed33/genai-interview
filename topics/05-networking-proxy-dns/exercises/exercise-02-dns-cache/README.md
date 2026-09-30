# Exercise 02 — Phonebook Memory (TTL cache + record check)

**Story:** Resolver hammers authoritative DNS for every request. Add TTL memory + validate record types.

## Task
In `solution.py`:
- `VALID` — set of the 9 record types (A, AAAA, CNAME, MX, TXT, NS, SRV, PTR, SOA); `check(rtype)` → bool
- `TTLCache(clock)` with `put(name, value, ttl)` / `get(name)` → value or `None` (expired/missing); `clock` is a callable (tests inject fake time)

## Acceptance
- `check("CNAME")` true, `check("HACK")` false; hit within TTL, `None` after; overwrite refreshes value+deadline
