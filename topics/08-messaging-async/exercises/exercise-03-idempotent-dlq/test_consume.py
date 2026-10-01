"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol08_ex03")


def test_flow():
    msgs = [{"id": "a", "body": "a"}, {"id": "p", "body": "poison"}, {"id": "a", "body": "a"}]
    done, dupes, dlq, runs = sol.consume(msgs)
    assert done == ["a"] and dupes == ["a"]
    assert dlq == [{"id": "p", "tries": 3, "error": "rotten mango"}]
    assert runs == 1 + 3  # one success + three poison tries
