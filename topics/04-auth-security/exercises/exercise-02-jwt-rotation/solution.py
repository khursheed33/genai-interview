"""Solution: short exp, jti blocklist, rotation kills the old slip."""

import time
import uuid

import jwt

SECRET = "test-secret"


def mint(sub, roles, mins, secret=SECRET):
    now = int(time.time())
    return jwt.encode(
        {
            "sub": sub,
            "roles": roles,
            "iat": now,
            "exp": now + int(mins * 60),
            "jti": uuid.uuid4().hex,
        },
        secret,
        algorithm="HS256",
    )


def verify(token, secret, revoked: set):
    try:
        claims = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    return None if claims.get("jti") in revoked else claims


def rotate(refresh_token, secret, revoked: set):
    claims = verify(refresh_token, secret, revoked)
    if not claims:
        return None
    revoked.add(claims["jti"])
    sub, roles = claims["sub"], claims["roles"]
    return mint(sub, roles, 10, secret), mint(sub, roles, 7 * 24 * 60, secret)
