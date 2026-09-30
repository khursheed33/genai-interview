"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol04_ex03")


def test_idor():
    asha = {"id": "asha", "roles": ["user"]}
    bob = {"id": "bob", "roles": ["user"]}
    root = {"id": "root", "roles": ["admin"]}
    assert sol.authorize(asha, 7)[0] == 200
    assert sol.authorize(bob, 7)[0] == 403
    assert sol.authorize(root, 7)[0] == 200
    assert sol.authorize(asha, 999) == (404, None)


def test_policy():
    o = {"region": "blr", "amount": 5000}
    good = {"role": "manager", "region": "blr"}
    assert sol.may_refund(good, o, 12)
    assert not sol.may_refund({"role": "viewer", "region": "blr"}, o, 12)
    assert not sol.may_refund({"role": "manager", "region": "del"}, o, 12)
    assert not sol.may_refund(good, {"region": "blr", "amount": 99_999}, 12)
    assert not sol.may_refund(good, o, 22)
