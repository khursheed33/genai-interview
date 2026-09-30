"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path

import pytest


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol06_ex03")


def test_atomic():
    db = sol.seed()
    sol.transfer(db, 1, 2, 30)
    assert sol.balances(db) == [70, 130]
    with pytest.raises(ValueError):
        sol.transfer(db, 1, 2, 999)
    assert sol.balances(db) == [70, 130]
