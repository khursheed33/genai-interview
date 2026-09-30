"""06_python_cache.py — one-line memo + TTL jar (stdlib + cachetools).

Run: uv run python topics/07-caching/examples/06_python_cache.py
"""

from functools import lru_cache

import cachetools

CALLS = {"n": 0}


@lru_cache(maxsize=128)
def price(item, qty):
    CALLS["n"] += 1
    return (100 if item == "dosa" else 50) * qty


assert price("dosa", 2) == 200
assert price("dosa", 2) == 200  # free!
assert CALLS["n"] == 1
print("lru_cache: 2nd identical call free | info:", price.cache_info())
price.cache_clear()


jar = cachetools.TTLCache(maxsize=1000, ttl=60)
jar["sess:abc"] = {"user": "asha"}
assert jar["sess:abc"]["user"] == "asha"
print("TTLCache: session jar with auto-expiry (per-pod L1!)")
print("OK — lru_cache memoizes args; TTLCache adds expiry; size BOTH (leaks kill!)")
