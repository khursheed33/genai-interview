"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol_dsa")
longest_unique = sol.longest_unique
top_k_freq = sol.top_k_freq
two_sum = sol.two_sum


def test_two_sum():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([1, 2, 3], 99) is None


def test_sliding():
    assert longest_unique("abcabcbb") == 3
    assert longest_unique("bbbbb") == 1


def test_topk():
    assert top_k_freq(["dosa", "idli", "dosa"], 1) == [("dosa", 2)]
