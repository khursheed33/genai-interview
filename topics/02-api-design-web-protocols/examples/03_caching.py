"""03_caching.py — 'same dosa as last time?' (ETag -> 304).

Run: uv run python topics/02-api-design-web-protocols/examples/03_caching.py
"""

import hashlib

MENU = {"dosa": 80, "idli": 50}
VERSION = "v42"


def etag(payload, version):
    h = hashlib.sha256(f"{payload}{version}".encode()).hexdigest()[:12]
    return f'"{h}"'


tag = etag(MENU, VERSION)
print("ETag:", tag)


def conditional_get(if_none_match=None):
    current = etag(MENU, VERSION)
    if if_none_match == current:
        return 304, {}, None  # Not Modified — empty body, bytes saved!
    return 200, {"ETag": current, "Cache-Control": "max-age=60"}, MENU


s, h, b = conditional_get()
assert s == 200 and "ETag" in h
s2, _, b2 = conditional_get(if_none_match=h["ETag"])
assert (s2, b2) == (304, None)
print("first: 200 + body, second: 304 empty. Bytes saved!")

# Cache-Control quick parse
cc = "max-age=60, must-revalidate"
assert "max-age=60" in cc and "no-store" not in cc
print("OK — ETag+If-None-Match -> 304; no-store for secrets, version URLs to purge")
