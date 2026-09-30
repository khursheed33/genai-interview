# Exercise 01 — Sector the Society (CIDR planner)

**Story:** New region `10.20.0.0/16`. Carve public/app/db, count beds, answer "is this IP ours?"

## Task
In `solution.py` (stdlib `ipaddress`):
- `usable(cidr)` → int (total − 2)
- `contains(cidr, ip)` → bool
- `carve(cidr, tiers)` → dict tier→subnet string, splitting evenly (use `subnets()` + prefix math; assume len(tiers) is a power of two)

## Acceptance
- `usable("10.20.0.0/16") == 65534`; `contains` true/false correctly
- `carve("10.20.0.0/16", ["public","app","db","mgmt"])` gives 4×`/18` with public first
