"""01_password_hashing.py — grinder with salt + pepper (stdlib PBKDF2; same rules as argon2/bcrypt).

Run: uv run python topics/04-auth-security/examples/01_password_hashing.py
"""

import hashlib
import hmac
import os

ITERS = 200_000
PEPPER = os.environ.get("PEPPER", "dev-pepper-ROTATE-IN-PROD")  # from Vault in prod!


def hash_pw(password: str, salt: bytes | None = None, iters: int = ITERS) -> str:
    salt = salt or os.urandom(16)  # RANDOM per user — rainbow tables die here
    dk = hashlib.pbkdf2_hmac("sha256", (PEPPER + password).encode(), salt, iters)
    return f"pbkdf2${iters}${salt.hex()}${dk.hex()}"


def verify(password: str, stored: str) -> bool:
    _, iters, salt_hex, _ = stored.split("$")
    candidate = hash_pw(password, bytes.fromhex(salt_hex), int(iters)).split("$")[-1]
    return hmac.compare_digest(candidate, stored.split("$")[-1])  # constant-time!


def needs_rehash(stored: str) -> bool:
    return int(stored.split("$")[1]) < ITERS  # cost bumped? upgrade on next login


h1, h2 = hash_pw("dosa123"), hash_pw("dosa123")
assert h1 != h2  # salts differ
assert verify("dosa123", h1) and not verify("dosa124", h1)
assert not needs_rehash(h1)
print("same pw, different hashes (salt). wrong pw rejected. timing-safe compare.")
print("OK — argon2id/bcrypt in prod; salt random, pepper in Vault, MD5 NEVER")
