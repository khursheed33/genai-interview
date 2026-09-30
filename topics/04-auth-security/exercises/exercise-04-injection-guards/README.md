# Exercise 04 — Five Thieves, Five Locks (injection + traversal + SSRF)

**Story:** Pen-test found: login bypass via `' OR '1'='1`, stored XSS in reviews, `../../` file read, webhook fetching cloud metadata, filename `; rm -rf` passed to shell. Lock all five.

## Task
In `solution.py` implement:
- `find_user(db_rows: list[tuple], email)` — exact-match ONLY (no SQL string building; simulate param binding over the row list)
- `render(text)` — `html.escape` it
- `safe_path(base: str, name: str)` — resolve + must stay under base, else `ValueError`
- `url_ok(url, allow: set)` — hostname in allowlist AND not a non-public literal IP, else `ValueError`
- `run_echo(payload)` — return payload via argv-list subprocess (no shell), proving metachars inert

## Acceptance
- `' OR '1'='1` matches nothing; `<script>` gone after render; `../../etc/passwd` raises; metadata URL raises; `; rm -rf /` returned inert
