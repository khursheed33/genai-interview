"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol02_ex01")
ROUTES = sol.ROUTES

VERBS = ("get", "create", "update", "delete", "fetch", "add")


def _find(method, path):
    return next((r for r in ROUTES if r["method"] == method and r["path"] == path), None)


def test_no_verbs_plural():
    for r in ROUTES:
        low = r["path"].lower()
        assert not any(f"/{v}" in low for v in VERBS), r
    assert any(r["path"] == "/orders" for r in ROUTES)


def test_methods_status():
    assert _find("POST", "/orders")["status"] == 201
    assert _find("GET", "/orders/{id}")["status"] == 200
    assert _find("PUT", "/orders/{id}")["status"] == 200
    assert _find("PATCH", "/orders/{id}")["status"] == 200
    assert _find("DELETE", "/orders/{id}")["status"] in (200, 204)


def test_covers_all():
    assert len(ROUTES) >= 6
