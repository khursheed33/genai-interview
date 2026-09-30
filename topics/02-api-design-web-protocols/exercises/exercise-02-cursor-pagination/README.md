# Exercise 02 — Cursor Pages That Don't Skip (opaque cursors)

**Story:** Admin scrolls orders with `?page=500`. It's slow and rows jump when new orders arrive. Ship cursor pagination.

## Task
In `solution.py` implement over the given `ITEMS` (ids 1..N):
- `encode(last_id) -> str` / `decode(cursor) -> int` (opaque! callers can't guess the scheme)
- `page(after=None, limit=3)` → `{"data": [...], "pageInfo": {"next": cursor|None, "hasMore": bool}}`

## Acceptance
- Walk all 10 items with `limit=3` → 4 pages, ids in order, no dupes/skips
- Cursor is opaque (not plain `"4"` — decode round-trips but isn't the raw id)
- `limit` larger than remainder → `hasMore is False`, `next is None`
