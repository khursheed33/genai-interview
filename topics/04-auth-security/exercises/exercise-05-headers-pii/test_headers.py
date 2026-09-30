"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol04_ex05")


def test_headers():
    h = sol.headers()
    assert h["X-Frame-Options"] == "DENY" and h["X-Content-Type-Options"] == "nosniff"
    assert "frame-ancestors 'none'" in h["Content-Security-Policy"]
    assert h["Strict-Transport-Security"].startswith("max-age=")


def test_masks_audit():
    assert sol.mask_email("asha@x.com") == "a***@x.com"
    assert sol.mask_card("4111-1111-1111-1234") == "****1234"
    rec = sol.audit(
        "op", "refund", "order:7", {"email": "a@x.com", "card": "4111111111111234", "note": "ok"}
    )
    assert rec["meta"] == {"email": "a***@x.com", "card": "****1234", "note": "ok"}
