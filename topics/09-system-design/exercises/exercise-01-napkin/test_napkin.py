"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol09_ex01")


def test_linkly():
    w = sol.write_rps(5_000_000, 3)
    assert 860 < w < 880, w
    assert sol.read_rps(5_000_000, 3) == w * 8
    assert 650 < sol.storage_gb(5_000_000 * 3 * 30, 500) < 700  # 450M x 500B x3!
    assert sol.bw_mbps(w * 8, 1000) > 40
    assert sol.boxes(w * 8) == 5  # 6944/2000*1.3 = 4.5 -> ceil 5
