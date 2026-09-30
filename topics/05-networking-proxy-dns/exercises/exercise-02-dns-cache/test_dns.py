"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol05_ex02")


def test_records():
    assert sol.check("CNAME") and sol.check("SOA") and len(sol.VALID) == 9
    assert not sol.check("HACK")


def test_ttl():
    t = {"n": 0.0}
    c = sol.TTLCache(clock=lambda: t["n"])
    c.put("a.shop", "1.2.3.4", ttl=300)
    assert c.get("a.shop") == "1.2.3.4"
    t["n"] += 300
    assert c.get("a.shop") is None
    c.put("a.shop", "5.6.7.8", ttl=60)
    assert c.get("a.shop") == "5.6.7.8"
