"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol09_ex03")


def test_roundtrip():
    for n in (0, 1, 61, 62, 3843, 123456789):
        s = sol.encode(n)
        assert set(s) <= set(sol.ALPHA) and sol.decode(s) == n


def test_allocator():
    a = sol.Allocator(10**6)
    ids = [a.next() for _ in range(5)]
    assert ids == [10**6 + 1, 10**6 + 2, 10**6 + 3, 10**6 + 4, 10**6 + 5]
    assert len({sol.encode(i) for i in ids}) == 5  # unique codes, no collision check needed!
