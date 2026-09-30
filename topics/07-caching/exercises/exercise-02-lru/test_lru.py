"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol07_ex02")


def test_evict():
    c = sol.LRU(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.get("b") is None and c.get("a") == 1 and c.get("c") == 3


def test_update_refresh():
    c = sol.LRU(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)  # refresh a
    c.put("c", 3)  # b flies now
    assert c.get("a") == 10 and c.get("b") is None and c.get("missing") is None
