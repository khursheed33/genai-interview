"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol02_ex05")


def _boom():
    raise RuntimeError("down")


def test_opens_and_fails_fast():
    t = {"n": 0.0}
    br = sol.Breaker(clock=lambda: t["n"])
    calls = {"n": 0}

    def counting_boom():
        calls["n"] += 1
        raise RuntimeError("down")

    for _ in range(3):
        assert br.call(counting_boom, lambda r: "FB") == "FB"
    assert br.state == "open"
    assert br.call(counting_boom, lambda r: "FB") == "FB"
    assert calls["n"] == 3  # open call never invoked fn


def test_probe_recovers():
    t = {"n": 0.0}
    br = sol.Breaker(clock=lambda: t["n"])
    for _ in range(3):
        br.call(_boom, lambda r: "FB")
    t["n"] += 11
    assert br.call(lambda: "back", lambda r: "FB") == "back"
    assert br.state == "closed"


def test_hmac():
    s, body = b"hook-secret", b'{"id":101}'
    assert sol.verify(s, body, sol.sign(s, body))
    assert not sol.verify(s, b"tampered", sol.sign(s, body))
