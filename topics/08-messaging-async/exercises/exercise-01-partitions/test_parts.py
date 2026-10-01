"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from itertools import chain
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol08_ex01")


def test_stable():
    assert sol.partition("asha", 8) == sol.partition("asha", 8)
    assert 0 <= sol.partition("asha", 8) < 8


def test_deal():
    got = sol.assign([0, 1, 2, 3], ["c1", "c2", "c3"])
    assert sorted(chain.from_iterable(got.values())) == [0, 1, 2, 3]
    assert got == {"c1": [0, 3], "c2": [1], "c3": [2]}
