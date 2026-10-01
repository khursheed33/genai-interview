"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol08_ex02")
M = sol.match


def test_star():
    assert M("order.*.blr", "order.paid.blr")
    assert not M("order.*.blr", "order.paid.del")
    assert not M("order.*.blr", "order.paid.blr.x")


def test_hash():
    assert M("order.#", "order.paid.blr.extra")
    assert M("order.#", "order.paid")
    assert M("#", "anything.at.all")
    assert M("a.#.c", "a.b.c") and M("a.#.c", "a.x.y.c") and not M("a.#.c", "a.x.y.d")
