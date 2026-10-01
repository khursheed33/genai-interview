"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol09_ex02")


def test_formulas():
    assert 9_500_000 < sol.bits(1_000_000, 0.01) < 9_700_000
    assert sol.hashes(sol.bits(1_000_000, 0.01), 1_000_000) == 7


def test_behavior():
    b = sol.Bloom(1000, p=0.01)
    for i in range(500):
        b.add(f"u:{i}")
    assert all(f"u:{i}" in b for i in range(500))
    fps = sum(1 for i in range(2000) if f"zz:{i}" in b)
    assert fps / 2000 < 0.05
