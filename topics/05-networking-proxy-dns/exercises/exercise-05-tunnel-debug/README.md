# Exercise 05 — Passages + Doctor (tunnel builder + debug router)

**Story:** On-call keeps fat-fingering `ssh -L` (prod outage!) and runs `tcpdump` before `ping`. Ship validated builders + a symptom router.

## Task
In `solution.py`:
- `tunnel(kind, **kw)` — kind in {"local","remote","socks"}; validate ports 1–65535 + hosts (no spaces/shell chars); return the exact command string
- `diagnose(symptom)` — map: "down?"→`ping`, "where-die"→`traceroute`, "wrong-ip"→`dig +trace`, "app-or-net"→`curl -v + timings`, "who-listens"→`ss -tlnp`, "raw-talk"→`telnet/nc`, "cert"→`openssl s_client`, "packets"→`tcpdump`; unknown → `"start with ping (cheap first)"`

## Acceptance
- `tunnel("local", ...)` builds `-L` string; bad port/host raises `ValueError`; all 8 symptoms route, unknown defaults
