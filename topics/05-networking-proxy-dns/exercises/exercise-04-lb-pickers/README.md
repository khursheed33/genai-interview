# Exercise 04 — Fair Counters (LB pickers + sticky)

**Story:** Big pod hogs traffic, WS rooms scatter on redeploy, drained node still served. Implement the picker set.

## Task
In `solution.py`:
- `rr(nodes, n)` → n picks round-robin; `least_conn(active: dict)` → min key
- `ip_hash(ip, nodes)` → stable node (hashlib, any algo); `healthy(nodes, is_up: dict)` → live list or raise `RuntimeError`
- `Sticky` class with `.route(user, nodes)` → stable pin per user

## Acceptance
- `rr(["a","b"], 5) == ["a","b","a","b","a"]`; least-conn picks min; same IP stable; unhealthy filtered; all-dead raises; sticky pins
