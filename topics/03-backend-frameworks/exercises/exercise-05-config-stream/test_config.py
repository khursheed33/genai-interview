"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
import types
from pathlib import Path

import pytest


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol03_ex05")


def test_failfast_mask():
    assert sol.Settings(env="dev").must_have_llm()
    with pytest.raises(ValueError):
        sol.Settings(env="prod", llm_key="").must_have_llm()
    s = sol.Settings(env="prod", llm_key="sk-live-9")
    assert "sk-live-9" not in s.masked() and s.masked().startswith("sk-")


def test_lazy_stream():
    g = sol.ndjson([{"a": 1}, {"b": 2}])
    assert isinstance(g, types.GeneratorType)
    assert list(g) == ['{"a": 1}\n', '{"b": 2}\n']
