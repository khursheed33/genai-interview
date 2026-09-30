"""Solution: hash fingerprint + If-None-Match compare."""

import hashlib


def etag(body: str) -> str:
    return f'"{hashlib.sha256(body.encode()).hexdigest()[:16]}"'


def serve(body, if_none_match=None):
    tag = etag(body)
    if if_none_match is not None and if_none_match == tag:
        return 304, {}, None
    return 200, {"ETag": tag}, body
