# Exercise 03 — 304 or Not? (ETag conditional GET)

**Story:** Mobile app re-downloads the full menu every 30s. Users on 2G suffer. Add ETags.

## Task
In `solution.py` implement:
- `etag(body: str) -> str` — stable fingerprint (any hash, quoted)
- `serve(body, if_none_match=None)` → `(status, headers, out_body)` — `304` + `None` body on match, else `200` + `ETag` header + body

## Acceptance
- Same body → same tag; different body → different tag
- Matching `If-None-Match` → `(304, ..., None)`; mismatch/missing → `(200, {"ETag": tag}, body)`
