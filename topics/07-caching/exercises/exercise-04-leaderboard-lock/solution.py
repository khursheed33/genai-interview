"""Solution: zset ranks, token lock guards — same commands as prod Redis."""

import uuid


def add_score(r, board, user, pts):
    return r.zincrby(board, pts, user)


def top(r, board, n):
    return [(m.decode(), s) for m, s in r.zrevrange(board, 0, n - 1, withscores=True)]


def acquire(r, key, ttl_ms=5000):
    token = uuid.uuid4().hex
    return token if r.set(key, token, nx=True, px=ttl_ms) else None


def release(r, key, token):
    if r.get(key) != token.encode():
        return False
    return bool(r.delete(key))
