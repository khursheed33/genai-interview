"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol09_ex05")


def test_storage():
    assert 60 < sol.vector_gb(1_000_000, 20, 768) < 63


def test_money_fleet():
    assert sol.monthly_cost(50_000, 3000, 2.0) == 9000.0
    assert sol.monthly_cost(50_000, 3000, 2.0, cache_hit=0.5) == 4500.0
    assert sol.gpus_needed(100, 2.0) == 200
