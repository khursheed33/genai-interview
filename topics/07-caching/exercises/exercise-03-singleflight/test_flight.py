"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
import threading
import time
from pathlib import Path

import pytest


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol07_ex03")


def test_one_flight():
    f, calls = sol.Flight(), {"n": 0}

    def slow():
        time.sleep(0.05)
        calls["n"] += 1
        return "menu"

    results = [None] * 20

    def one(idx):
        results[idx] = f.get("blr", slow)

    ts = [threading.Thread(target=one, args=(i,)) for i in range(20)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert calls["n"] == 1 and all(r == "menu" for r in results)


def test_error_not_cached():
    f, calls = sol.Flight(), {"n": 0}

    def bad():
        calls["n"] += 1
        raise RuntimeError("db down")

    with pytest.raises(RuntimeError):
        f.get("k", bad)
    with pytest.raises(RuntimeError):
        f.get("k", bad)
    assert calls["n"] == 2
