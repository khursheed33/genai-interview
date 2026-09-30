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


sol = _load("sol_retry")
retry = sol.retry


def test_eventual_success():
    calls = {"n": 0}

    @retry(times=3)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("hiccup")
        return "paid"

    assert flaky() == "paid"
    assert flaky.__name__ == "flaky"


def test_gives_up():
    calls = {"n": 0}

    @retry(times=3)
    def always_bad():
        calls["n"] += 1
        raise ValueError("down")

    with pytest.raises(ValueError):
        always_bad()
    assert calls["n"] == 3
