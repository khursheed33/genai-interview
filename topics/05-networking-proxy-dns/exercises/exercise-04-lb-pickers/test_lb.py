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


sol = _load("sol05_ex04")


def test_pickers():
    assert sol.rr(["a", "b"], 5) == ["a", "b", "a", "b", "a"]
    assert sol.least_conn({"a": 5, "b": 1}) == "b"
    assert sol.ip_hash("9.9.9.9", ["a", "b", "c"]) == sol.ip_hash("9.9.9.9", ["a", "b", "c"])


def test_health_sticky():
    assert sol.healthy(["a", "b"], {"a": True, "b": False}) == ["a"]
    with pytest.raises(RuntimeError):
        sol.healthy(["a"], {"a": False})
    s = sol.Sticky()
    assert s.route("asha", ["a", "b"]) == s.route("asha", ["a", "b"])
