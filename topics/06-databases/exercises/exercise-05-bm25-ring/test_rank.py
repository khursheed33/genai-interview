"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol06_ex05")
DOCS = {1: "crispy dosa chutney", 2: "idli poha", 3: "dosa dosa dosa festival menu"}


def test_rank():
    assert sol.bm25_rank("dosa", DOCS) == [3, 1]
    assert sol.bm25_rank("idli", DOCS) == [2]


def test_ring():
    keys = [f"u:{i}" for i in range(200)]
    assert sol.moved_fraction(keys, ["n1", "n2", "n3"], ["n1", "n2", "n3", "n4"]) < 0.45
