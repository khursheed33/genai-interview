"""04_oauth_pkce.py — valet key ceremony (S256) + scope guard.

Run: uv run python topics/04-auth-security/examples/04_oauth_pkce.py
"""

import base64
import hashlib
import os
import time

CODES: dict[str, dict] = {}


def gen_verifier(n=64):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    return "".join(alphabet[b % len(alphabet)] for b in os.urandom(n))


def challenge_of(verifier: str) -> str:
    return (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    )


def issue_code(client_id, challenge, scopes):
    code = os.urandom(12).hex()
    CODES[code] = {
        "client_id": client_id,
        "challenge": challenge,
        "scopes": set(scopes),
        "exp": time.time() + 600,
        "used": False,
    }
    return code


def redeem(code, verifier, client_id):
    c = CODES.get(code)
    if not c or c["used"] or c["exp"] < time.time() or c["client_id"] != client_id:
        return None
    if challenge_of(verifier) != c["challenge"]:
        return None  # stolen code without verifier = useless paper
    c["used"] = True  # single-use!
    return {"access": "tok_" + os.urandom(6).hex(), "scopes": sorted(c["scopes"])}


def can(token_scopes, needed):
    return needed in token_scopes  # server enforces per endpoint; UI hiding is NOT security


v = gen_verifier()
ch = challenge_of(v)
assert challenge_of(v) == ch and v != ch
code = issue_code("swiggy-app", ch, ["orders:read"])
assert redeem(code, "wrong-verifier", "swiggy-app") is None
tok = redeem(code, v, "swiggy-app")
assert tok and can(tok["scopes"], "orders:read") and not can(tok["scopes"], "refund:write")
assert redeem(code, v, "swiggy-app") is None  # replay dead
print("OK — PKCE binds code to verifier; codes single-use+expiring; scopes enforced server-side")
