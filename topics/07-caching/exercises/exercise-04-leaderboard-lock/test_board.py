"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path

import fakeredis


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol07_ex04")


def test_board():
    r = fakeredis.FakeStrictRedis()
    assert sol.add_score(r, "lb", "asha", 100) == 100.0
    assert sol.add_score(r, "lb", "asha", 50) == 150.0
    sol.add_score(r, "lb", "bob", 500)
    assert sol.top(r, "lb", 2) == [("bob", 500.0), ("asha", 150.0)]


def test_lock():
    r = fakeredis.FakeStrictRedis()
    t = sol.acquire(r, "k")
    assert t and sol.acquire(r, "k") is None
    assert sol.release(r, "k", "nope") is False
    assert sol.release(r, "k", t) is True
    assert sol.acquire(r, "k") is not None
