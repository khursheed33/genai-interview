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


sol = _load("sol05_ex03")


def test_headers():
    h = sol.forward_headers("1.1.1.1")
    assert h == {"X-Forwarded-For": "1.1.1.1", "X-Forwarded-Proto": "http", "X-Request-ID": "req_1"}
    chained = sol.forward_headers("10.0.0.5", existing="1.1.1.1")
    assert chained["X-Forwarded-For"] == "1.1.1.1, 10.0.0.5"


def test_pick():
    ups = [{"url": "a", "dead_until": 99.0}, {"url": "b", "dead_until": 0.0}]
    assert sol.pick(ups, now=10.0)["url"] == "b"
    with pytest.raises(RuntimeError):
        sol.pick([{"url": "a", "dead_until": 999.0}], now=100.0)
