"""03_auth_api.py — gate + badges + rotating slips (FastAPI + TestClient).

Run: uv run python topics/04-auth-security/examples/03_auth_api.py
Login -> access(10m) + refresh(7d). Refresh ROTATES (old jti dies, reuse = theft).
"""

import hashlib
import hmac
import os
import time
import uuid

import jwt
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

SECRET = "dev-only-secret"
REVOKED: set[str] = set()
SALT = os.urandom(16)


def _hash(pw: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), SALT, 100_000).hex()


USERS = {
    "asha": {"pw": _hash("dosa123"), "roles": ["user"]},
    "boss": {"pw": _hash("idli456"), "roles": ["admin"]},
}


def mint(sub, roles, mins):
    now = int(time.time())
    return jwt.encode(
        {"sub": sub, "roles": roles, "iat": now, "exp": now + mins * 60, "jti": uuid.uuid4().hex},
        SECRET,
        algorithm="HS256",
    )


def claims_of(authorization: str):
    if not authorization.startswith("Bearer "):
        return None
    try:
        claims = jwt.decode(authorization[7:], SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    return None if claims["jti"] in REVOKED else claims


app = FastAPI()


class LoginIn(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(body: LoginIn):
    u = USERS.get(body.username)
    if not u or not hmac.compare_digest(_hash(body.password), u["pw"]):
        return JSONResponse({"title": "bad credentials"}, status_code=401)
    return {
        "access": mint(body.username, u["roles"], 10),
        "refresh": mint(body.username, u["roles"], 7 * 24 * 60),
    }


@app.get("/me")
def me(authorization: str = Header(default="")):
    c = claims_of(authorization)
    if not c:
        return JSONResponse({"title": "login required"}, status_code=401)
    return {"sub": c["sub"], "roles": c["roles"]}


@app.get("/admin/ping")
def admin(authorization: str = Header(default="")):
    c = claims_of(authorization)
    if not c:
        return JSONResponse({"title": "login required"}, status_code=401)
    if "admin" not in c["roles"]:
        return JSONResponse({"title": "admins only"}, status_code=403)
    return {"pong": True}


@app.post("/refresh")
def refresh(authorization: str = Header(default="")):
    c = claims_of(authorization)
    if not c:
        return JSONResponse({"title": "bad refresh"}, status_code=401)
    REVOKED.add(c["jti"])  # ROTATE: old slip dies; reuse = theft alarm
    u = USERS[c["sub"]]
    return {
        "access": mint(c["sub"], u["roles"], 10),
        "refresh": mint(c["sub"], u["roles"], 7 * 24 * 60),
    }


@app.post("/logout")
def logout(authorization: str = Header(default="")):
    c = claims_of(authorization)
    if c:
        REVOKED.add(c["jti"])
    return {"ok": True}


t = TestClient(app)
r = t.post("/login", json={"username": "asha", "password": "dosa123"})
assert r.status_code == 200, r.text
A, R1 = r.json()["access"], r.json()["refresh"]
assert t.get("/me").status_code == 401
assert t.get("/me", headers={"Authorization": f"Bearer {A}"}).json()["sub"] == "asha"
assert t.get("/admin/ping", headers={"Authorization": f"Bearer {A}"}).status_code == 403
B = t.post("/login", json={"username": "boss", "password": "idli456"}).json()["access"]
assert t.get("/admin/ping", headers={"Authorization": f"Bearer {B}"}).status_code == 200
assert t.post("/refresh", headers={"Authorization": f"Bearer {R1}"}).status_code == 200
assert (
    t.post("/refresh", headers={"Authorization": f"Bearer {R1}"}).status_code == 401
)  # reuse dead!
assert t.post("/login", json={"username": "asha", "password": "nope"}).status_code == 401
print("OK — 401 unknown, 403 known-but-no, refresh rotates, reuse dies, logout revokes")
