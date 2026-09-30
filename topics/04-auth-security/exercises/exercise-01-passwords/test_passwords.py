"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol04_ex01")


def test_salt_verify():
    assert sol.hash_pw("dosa123") != sol.hash_pw("dosa123")
    h = sol.hash_pw("dosa123")
    assert sol.verify("dosa123", h) and not sol.verify("dosa124", h)


def test_rehash():
    assert sol.needs_rehash(sol.hash_pw("x", iters=10_000))
    assert not sol.needs_rehash(sol.hash_pw("x"))
