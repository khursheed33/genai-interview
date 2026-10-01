"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol08_ex04")


def test_happy():
    assert sol.run("o1") == ("done", [])


def test_compensate_reverse():
    status, comp = sol.run("o2", fail_at="stock")
    assert status == "failed:stock" and comp == ["pay"]
    status, comp = sol.run("o3", fail_at="ship")
    assert status == "failed:ship" and comp == ["stock", "pay"]
