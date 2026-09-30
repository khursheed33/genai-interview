"""02_jwt_hs_rs.py — sealed slips: shared secret vs seal-stamp.

Run: uv run python topics/04-auth-security/examples/02_jwt_hs_rs.py
"""

import time

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# --- HS256: one shared secret ---
HS_SECRET = "dev-secret-ROTATE-VIA-VAULT"
hs = jwt.encode(
    {"sub": "123", "role": "user", "exp": int(time.time()) + 600}, HS_SECRET, algorithm="HS256"
)
assert jwt.decode(hs, HS_SECRET, algorithms=["HS256"])["sub"] == "123"
print("HS256 ok:", hs[:30], "...")

# tampered payload? signature mismatch!
parts = hs.split(".")
try:
    jwt.decode(parts[0] + "." + parts[1] + "X." + parts[2], HS_SECRET, algorithms=["HS256"])
    raise AssertionError("tamper passed?!")
except jwt.InvalidTokenError:
    print("tampered token rejected (signature mismatch)")

# expired? rejected. wrong alg (alg:none confusion)? rejected.
old = jwt.encode({"sub": "1", "exp": int(time.time()) - 5}, HS_SECRET, algorithm="HS256")
for bad in (old, hs):
    try:
        jwt.decode(bad, HS_SECRET, algorithms=["RS256"] if bad is hs else ["HS256"])
        if bad is hs:
            raise AssertionError("alg confusion passed?!")
    except jwt.InvalidTokenError as e:
        print("rejected as expected:", type(e).__name__)

# --- RS256: private seals, world verifies ---
priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub = priv.public_key()
priv_pem = priv.private_bytes(
    serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
)
pub_pem = pub.public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
)
rs = jwt.encode(
    {"sub": "7", "role": "admin", "exp": int(time.time()) + 600}, priv_pem, algorithm="RS256"
)
got = jwt.decode(rs, pub_pem, algorithms=["RS256"])
assert got["role"] == "admin"
print("RS256 ok — 5 microservices verify with PUBLIC key; private stays in KMS/HSM")
print("OK — short exp, check aud/iss in prod, whitelist alg, jti for revocation")
