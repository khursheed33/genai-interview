"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol08_ex05")
EVS = [("credit", 50), ("debit", 30), ("credit", 20), ("debit", 5)]


def test_fold_snap():
    assert sol.fold(EVS) == 35
    assert sol.with_snapshot(EVS, every=2) == {2: 20, 4: 35}


def test_time_travel():
    snaps = sol.with_snapshot(EVS, every=2)
    assert sol.balance_at(EVS, snaps, 3) == 40
    assert sol.balance_at(EVS, snaps, 2) == 20
    assert sol.balance_at(EVS, snaps, 4) == 35
