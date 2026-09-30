"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol02_ex02")


def test_walk_all():
    seen, after, pages = [], None, 0
    while True:
        out = sol.page(after=after, limit=3)
        seen += [o["id"] for o in out["data"]]
        pages += 1
        if not out["pageInfo"]["hasMore"]:
            assert out["pageInfo"]["next"] is None
            break
        after = out["pageInfo"]["next"]
    assert seen == list(range(1, 11))
    assert pages == 4


def test_opaque():
    c = sol.encode(4)
    assert c != "4" and sol.decode(c) == 4
