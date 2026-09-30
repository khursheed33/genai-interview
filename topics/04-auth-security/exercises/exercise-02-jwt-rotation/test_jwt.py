"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
import time
from pathlib import Path

import jwt as pyjwt


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol04_ex02")
S = sol.SECRET


def test_roundtrip_tamper_expiry():
    revoked = set()
    t = sol.mint("asha", ["user"], 10, S)
    assert sol.verify(t, S, revoked)["sub"] == "asha"
    assert sol.verify(t[:-2] + "XX", S, revoked) is None
    old = pyjwt.encode({"sub": "x", "jti": "j1", "exp": int(time.time()) - 5}, S, algorithm="HS256")
    assert sol.verify(old, S, revoked) is None


def test_rotate_reuse_logout():
    revoked = set()
    a = sol.mint("asha", ["user"], 10, S)
    r1 = sol.mint("asha", ["user"], 7 * 24 * 60, S)
    pair = sol.rotate(r1, S, revoked)
    assert pair and sol.verify(pair[0], S, revoked)
    assert sol.rotate(r1, S, revoked) is None  # reuse dead
    revoked.add(sol.verify(a, S, revoked)["jti"])  # logout
    assert sol.verify(a, S, revoked) is None
