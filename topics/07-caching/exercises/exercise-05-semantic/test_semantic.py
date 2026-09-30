"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol07_ex05")


def test_normalize():
    assert sol.normalize("  Refund Policy?! ") == "refund policy"


def test_semantic():
    c = sol.SemanticCache()
    c.put("how do i get money back for my order", "Refund in 3-5 days.")
    ans, how = c.ask("How do I get my money back for the order?!")
    assert ans == "Refund in 3-5 days." and how.startswith("semantic")
    assert c.ask("how do i get money back for my order")[1] == "exact"
    assert c.ask("dosa price today")[1] == "miss"
