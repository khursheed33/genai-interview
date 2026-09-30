"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import asyncio
import importlib.util
import time
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol_async_parallel")
run_all = sol.run_all
run_limited = sol.run_limited


def test_parallel_faster():
    t0 = time.perf_counter()
    out = asyncio.run(run_all(["a", "b"], delay=0.2))
    dt = time.perf_counter() - t0
    assert out == ["a done", "b done"]
    assert dt < 0.35


def test_limited_respects_cap():
    current = {"n": 0, "peak": 0}
    orig = sol.fake_call

    async def tracked(name, delay=0.1):
        current["n"] += 1
        current["peak"] = max(current["peak"], current["n"])
        try:
            return await orig(name, delay)
        finally:
            current["n"] -= 1

    sol.fake_call = tracked
    try:
        out = asyncio.run(run_limited([f"q{i}" for i in range(5)], limit=2, delay=0.1))
    finally:
        sol.fake_call = orig
    assert len(out) == 5
    assert current["peak"] <= 2
