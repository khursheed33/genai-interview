"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol06_ex04")


def test_chain():
    out = sol.project(
        sol.sort_desc(sol.group_sum(sol.match(sol.DOCS, item="dosa"), "city", "amount"), "total"),
        "_id",
        "total",
    )
    assert out == [{"_id": "blr", "total": 350}, {"_id": "del", "total": 300}]


def test_stages():
    assert sol.match(sol.DOCS, city="del") == [sol.DOCS[2]]
    assert sol.project([{"a": 1, "b": 2}], "a") == [{"a": 1}]
