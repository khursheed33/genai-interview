"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol05_ex01")


def test_counts():
    assert sol.usable("10.20.0.0/16") == 65534
    assert sol.contains("10.20.0.0/16", "10.20.200.9")
    assert not sol.contains("10.20.0.0/16", "11.0.0.1")


def test_carve():
    plan = sol.carve("10.20.0.0/16", ["public", "app", "db", "mgmt"])
    assert list(plan) == ["public", "app", "db", "mgmt"]
    assert all(s.endswith("/18") for s in plan.values())
    assert plan["public"] == "10.20.0.0/18"
