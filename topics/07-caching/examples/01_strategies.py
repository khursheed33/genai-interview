"""01_strategies.py — five tiffin habits, with hit/miss counters.

Run: uv run python topics/07-caching/examples/01_strategies.py
"""

DB = {"menu:blr": ["dosa", "idli"]}
FETCHES = {"n": 0}


def db_read(k):
    FETCHES["n"] += 1
    return DB[k]


def db_write(k, v):
    DB[k] = v


# --- cache-aside: check, miss->fill, write->DELETE (never update!) ---
cache = {}


def aside_get(k):
    if k in cache:
        return cache[k], "hit"
    v = db_read(k)
    cache[k] = v
    return v, "miss"


def aside_set(k, v):
    db_write(k, v)
    cache.pop(k, None)  # delete, don't update (kills write-race staleness!)


assert aside_get("menu:blr")[1] == "miss" and aside_get("menu:blr")[1] == "hit"
aside_set("menu:blr", ["dosa"])
assert "menu:blr" not in cache and FETCHES["n"] == 1
print("aside: miss->fill, write deletes; DB fetches:", FETCHES["n"])

# --- write-through: fresh reads, 2x write cost ---
wt_cache, wt_db, COST = {}, {}, {"w": 0}


def wt_write(k, v):
    wt_cache[k] = v
    wt_db[k] = v
    COST["w"] += 2


wt_write("a", 1)
assert wt_cache["a"] == wt_db["a"] == 1 and COST["w"] == 2
print("write-through: cache+DB together (fresh, 2x write cost)")

# --- write-behind: fast ack, async flush (losable only!) ---
wb_cache, wb_db, PENDING = {}, {}, []


def wb_write(k, v):
    wb_cache[k] = v
    PENDING.append(k)  # flush worker drains later


def flush():
    while PENDING:
        k = PENDING.pop(0)
        wb_db[k] = wb_cache[k]


wb_write("c", 5)
assert "c" not in wb_db  # not yet!
flush()
assert wb_db["c"] == 5
print("write-behind: ack fast, flush later (crash-before-flush = LOST — counters only!)")
print("OK — aside+TTL default; through for fresh; behind for losable; refresh-ahead for hot")
