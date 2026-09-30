"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol06_ex02")


def test_scan_to_search():
    db = sol.seed()
    assert "SCAN" in sol.plan(db)
    sol.fix(db)
    p = sol.plan(db)
    assert "SEARCH" in p and "USING INDEX" in p, p
