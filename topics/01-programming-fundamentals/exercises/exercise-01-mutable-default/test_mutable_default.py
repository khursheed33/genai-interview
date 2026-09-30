"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol_mutable_default")
add_student = sol.add_student


def test_no_leak():
    assert add_student("a") == ["a"]
    assert add_student("b") == ["b"]


def test_own_list():
    assert add_student("c", ["x"]) == ["x", "c"]
