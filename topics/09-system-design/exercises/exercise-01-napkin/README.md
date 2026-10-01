# Exercise 01 — Napkin for Linkly (QPS/storage/BW/boxes)

**Story:** Linkly: 5M DAU × 3 links/day, reads 8:1, 500B rows, 1KB responses. Size it.

## Task
In `solution.py` implement with `DAY = 86400`:
- `write_rps(dau, per_day, peak=5)`, `read_rps(...)` (×ratio), `storage_gb(urls_per_month, bytes_each, replicas=3)`, `bw_mbps(rps_n, bytes_each)`, `boxes(peak_rps, per_box=2000, headroom=1.3)` → ceil

## Acceptance
- Writes ≈ 868/s peak; reads 8×; monthly storage ≈ 675GB (450M × 500B × 3 replicas); boxes sane (peak/2000×1.3 rounded UP)
