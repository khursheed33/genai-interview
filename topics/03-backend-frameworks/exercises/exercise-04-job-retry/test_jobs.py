"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path

import pytest


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol03_ex04")


def test_retry_counts():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("hiccup")
        return "ok"

    assert sol.run_with_retry(flaky) == ("ok", 3)

    bad_calls = {"n": 0}

    def bad():
        bad_calls["n"] += 1
        raise ValueError("down")

    with pytest.raises(ValueError):
        sol.run_with_retry(bad)
    assert bad_calls["n"] == 3


def test_idempotent_dlq():
    done, dlq, calls = set(), [], {"n": 0}

    def once():
        calls["n"] += 1
        return "ok"

    assert sol.process_once("j1", once, done, dlq) == "done"
    assert sol.process_once("j1", once, done, dlq) == "duplicate"
    assert calls["n"] == 1
    assert sol.process_once("j9", lambda: 1 / 0, done, dlq) == "failed"
    assert dlq and dlq[0][0] == "j9"
