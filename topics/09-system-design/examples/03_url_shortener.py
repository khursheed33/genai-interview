"""03_url_shortener.py — hello-world system: counter + base62 + cache (TestClient!).

Run: uv run python topics/09-system-design/examples/03_url_shortener.py
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

ALPHA = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62(n):
    if n == 0:
        return "0"
    out = ""
    while n:
        n, r = divmod(n, 62)
        out = ALPHA[r] + out
    return out


def base62_decode(s):
    n = 0
    for ch in s:
        n = n * 62 + ALPHA.index(ch)
    return n


assert base62_decode(base62(123456789)) == 123456789
print("base62 roundtrip: 123456789 <->", base62(123456789))

app = FastAPI()
IDS = {"n": 10**6}  # range allocator: box grabs 1M IDs in RAM (no per-write coordination!)
URLS, CACHE = {}, {}


@app.post("/v1/urls", status_code=201)
def shorten(body: dict):
    IDS["n"] += 1
    short = base62(IDS["n"])
    URLS[short] = body["long"]
    return {"short": short}


@app.get("/{short}")
def redir(short: str):
    if short in CACHE:  # hot 20% served from RAM!
        return {"to": CACHE[short], "via": "cache"}
    if short not in URLS:
        return JSONResponse({"title": "unknown"}, status_code=404)
    CACHE[short] = URLS[short]
    return {"to": URLS[short], "via": "db"}  # (prod: 301 + browser caches!)


t = TestClient(app)
r = t.post("/v1/urls", json={"long": "https://shop.com/mega-sale"})
assert r.status_code == 201
s = r.json()["short"]
assert t.get(f"/{s}").json()["via"] == "db"
assert t.get(f"/{s}").json()["via"] == "cache"  # 2nd hit hot!
assert t.get("/nope").status_code == 404
print("short:", s, "| db then cache | 404 ghosts")
print("OK — counter+base62 (no collisions!), 301+cache reads, quota+auth at gate!")
