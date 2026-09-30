"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
import random
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol02_ex04")


def test_bucket():
    t = {"n": 0.0}
    b = sol.Bucket(rate=2, burst=2, clock=lambda: t["n"])
    assert b.allow() and b.allow() and not b.allow()
    t["n"] += 1.0
    assert b.allow() and b.allow() and not b.allow()


def test_backoff_bounds():
    rng = random.Random(7)
    assert 0.25 <= sol.backoff(0, rng=rng) <= 0.5
    assert sol.backoff(10, rng=rng) <= 8.0
    assert sol.wait_for(5, 0.5) == 5
    assert sol.wait_for(None, 0.5) == 0.5
