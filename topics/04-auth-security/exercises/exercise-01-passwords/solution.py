"""Solution: random salt per user, constant-time verify, cost upgrades on login."""

import hashlib
import hmac
import os

ITERS = 200_000


def hash_pw(password, salt=None, iters=ITERS):
    salt = salt if salt is not None else os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iters)
    return f"pbkdf2${iters}${salt.hex()}${dk.hex()}"


def verify(password, stored):
    _, iters, salt_hex, want = stored.split("$")
    got = hash_pw(password, bytes.fromhex(salt_hex), int(iters)).split("$")[-1]
    return hmac.compare_digest(got, want)


def needs_rehash(stored):
    return int(stored.split("$")[1]) < ITERS
