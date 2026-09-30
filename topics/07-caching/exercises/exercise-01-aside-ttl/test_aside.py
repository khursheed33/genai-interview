"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol07_ex01")


def test_aside():
    t = {"n": 0.0}
    c = sol.AsideCache({"m": ["dosa"]}, clock=lambda: t["n"])
    assert c.get("m") == ["dosa"] and c.get("m") == ["dosa"]
    assert (c.hits, c.misses) == (1, 1)
    c.set("m", ["idli"])
    assert c.get("m") == ["idli"] and c.misses == 2  # write deleted -> refill
    t["n"] += 61
    assert c.get("m") == ["idli"] and c.misses == 3  # expired -> refill
