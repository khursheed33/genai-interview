"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol02_ex03")


def test_stable():
    assert sol.etag("dosa") == sol.etag("dosa")
    assert sol.etag("dosa") != sol.etag("idli")


def test_conditional():
    s, h, b = sol.serve("menu-v1")
    assert s == 200 and b == "menu-v1" and "ETag" in h
    s2, _, b2 = sol.serve("menu-v1", if_none_match=h["ETag"])
    assert (s2, b2) == (304, None)
    s3, _, _ = sol.serve("menu-v2", if_none_match=h["ETag"])
    assert s3 == 200
