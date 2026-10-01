"""Solution: avg -> xpeak -> xreplicas -> xheadroom (always ceil boxes!)."""

import math

DAY = 86400


def write_rps(dau, per_day, peak=5):
    return dau * per_day / DAY * peak


def read_rps(dau, per_day, ratio=8, peak=5):
    return write_rps(dau, per_day, peak) * ratio


def storage_gb(urls_per_month, bytes_each, replicas=3):
    return urls_per_month * bytes_each * replicas / 1e9


def bw_mbps(rps_n, bytes_each):
    return rps_n * bytes_each * 8 / 1e6


def boxes(peak_rps, per_box=2000, headroom=1.3):
    return math.ceil(peak_rps / per_box * headroom)
