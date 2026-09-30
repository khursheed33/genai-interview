# Exercise 03 — Receptionist's Stamp (proxy headers + sick upstream)

**Story:** App logs show every client as `10.0.0.5` (the proxy!) and dead pods still get traffic. Fix the forwarder.

## Task
In `solution.py`:
- `forward_headers(client_ip, proto="http", req_id="req_1")` → dict with `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Request-ID`
- `pick(upstreams)` → first with `dead_until <= now` (each upstream: `{"url", "dead_until"}`); `now` param injectable; raise `RuntimeError` if none (caller maps to 503)

## Acceptance
- Headers exact; proxy chain appends (`X-Forwarded-For: "1.1.1.1, 10.0.0.5"` when helper takes existing)
- Sick upstream skipped; all dead → `RuntimeError`
