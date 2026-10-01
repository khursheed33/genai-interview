"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol09_ex04")


def test_quorum():
    assert sol.quorum_ok(3, 2, 2) and not sol.quorum_ok(3, 1, 1)
    assert sol.quorum_ok(5, 3, 3)


def test_raft():
    nodes = ["a", "b", "c", "d"]
    t, w = sol.run_term(nodes, [("a", "a"), ("a", "b"), ("c", "c"), ("c", "d")])
    assert t == {"a": 2, "c": 2} and w == []
    t, w = sol.run_term(nodes, [("a", "a"), ("a", "b"), ("a", "c"), ("c", "d")])
    assert w == ["a"]
