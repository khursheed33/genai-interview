"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
import sys
import types
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol_generator")
active_orders = sol.active_orders
line_stream = sol.line_stream


def test_lazy():
    g = line_stream(5)
    assert isinstance(g, types.GeneratorType)
    assert list(g)[:2] == ["order-0", "order-1"]


def test_filter():
    assert list(active_orders(["order-1", "CANCELLED-2", "order-3"])) == ["order-1", "order-3"]


def test_memory():
    assert sys.getsizeof(line_stream(1_000_000)) < 1000
