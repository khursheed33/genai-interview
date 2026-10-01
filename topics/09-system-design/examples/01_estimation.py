"""01_estimation.py — napkin math toolkit + classic answers (prove numbers, don't chant!).

Run: uv run python topics/09-system-design/examples/01_estimation.py
"""

DAY = 86400


def rps(dau, per_user_day, peak_factor=5):
    return dau * per_user_day / DAY * peak_factor


def storage_gb(n_units, bytes_each, replicas=3):
    return n_units * bytes_each * replicas / 1e9


def bw_mbps(rps_n, bytes_each):
    return rps_n * bytes_each * 8 / 1e6


# URL shortener: 10M DAU x 2 links, 10:1 reads
writes = rps(10_000_000, 2)
reads = writes * 10
print(f"shortener: {writes:.0f} writes/s, {reads:.0f} reads/s")
assert 1000 < writes < 1500
monthly_urls = 10_000_000 * 2 * 30
print(f"storage/mo: {storage_gb(monthly_urls, 500):.0f} GB (x3 replicas!)")
assert 800 < storage_gb(monthly_urls, 500) < 1000
print(f"read BW: {bw_mbps(reads, 1000):.0f} Mbps")
assert rps(1_000_000, 10, peak_factor=1) < rps(1_000_000, 10, peak_factor=5)  # peak matters!

# nines table: DOWN minutes per YEAR (525600 * (1 - slo))
NINES_YEAR = {slo: 525600 * (1 - slo) for slo in (0.99, 0.999, 0.9999, 0.99999)}
assert round(NINES_YEAR[0.999]) == 526  # 8.7h/yr
assert round(NINES_YEAR[0.9999]) == 53  # 52min/yr
monthly_budget_min = 30 * 24 * 60 * 0.001
print(f"99.9%: {NINES_YEAR[0.999] / 60:.1f}h/yr down, {monthly_budget_min:.0f}min/mo error budget!")
print("OK — ask DAU/read-write/size/retention -> avg x5 peak -> storage x3 -> BW -> boxes!")
