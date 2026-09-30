"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol03_ex02")


def test_clamp():
    assert sol.clamp_limit(10**6) == 100
    assert sol.clamp_limit(-5) == 1
    assert sol.clamp_limit(20) == 20


def test_slice():
    out = sol.paginate(list(range(50)), limit=5, offset=10)
    assert out["data"] == [10, 11, 12, 13, 14] and out["total"] == 50
