"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol06_ex01")


def test_ranking():
    rows = sol.top_spenders(sol.seed())
    assert rows == [("bob", 500, 1, 800), ("asha", 300, 2, 800)], rows
    assert all(r[0] != "cara" for r in rows)
