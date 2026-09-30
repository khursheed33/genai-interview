"""Loads sibling solution.py via importlib (unique module name per exercise)."""

import importlib.util
from pathlib import Path

import pytest
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError


def _load(name):
    p = Path(__file__).parent / "solution.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sol = _load("sol03_ex03")


def _seeded():
    db, engine = sol.make_session()
    repo = sol.UserRepo(db)
    repo.create("asha", "a@x.com")
    repo.create("bob", "b@x.com")
    db.add(sol.Order(item="dosa", user_id=1))
    db.add(sol.Order(item="idli", user_id=1))
    db.commit()
    return db, engine, repo


def test_roundtrip_duplicate():
    db, _engine, repo = _seeded()
    assert repo.get(1)["email"] == "a@x.com"
    assert repo.get(999) is None
    with pytest.raises(IntegrityError):
        db.rollback()
        repo.create("clone", "a@x.com")
    db.rollback()
    assert sol.to_status(IntegrityError("x", "y", Exception("z"))) == 409
    assert sol.to_status(ValueError("boom")) == 500


def test_eager_two_queries():
    _db, engine, repo = _seeded()
    count = {"n": 0}

    @event.listens_for(engine, "before_cursor_execute")
    def _c(conn, cur, stmt, params, ctx, mp):
        count["n"] += 1

    try:
        out = repo.list_with_orders()
    finally:
        event.remove(engine, "before_cursor_execute", _c)
    assert sorted((o["name"], o["n_orders"]) for o in out) == [("asha", 2), ("bob", 0)]
    assert count["n"] <= 2, count
