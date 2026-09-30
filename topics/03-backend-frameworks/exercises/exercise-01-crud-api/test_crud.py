"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol03_ex01")


def _client():
    return TestClient(sol.build_app())


def test_create_get():
    c = _client()
    r = c.post("/orders", json={"email": "a@x.com", "items": ["dosa"]})
    assert r.status_code == 201 and r.json()["id"] == 1
    assert c.get("/orders/1").json()["items"] == ["dosa"]


def test_ghost_empty():
    c = _client()
    assert c.get("/orders/999").status_code == 404
    assert c.post("/orders", json={"email": "a@x.com", "items": []}).status_code == 422
