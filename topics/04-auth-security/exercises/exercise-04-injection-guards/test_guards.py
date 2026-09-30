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


sol = _load("sol04_ex04")
ROWS = [("a@x.com",), ("b@x.com",)]
ALLOW = {"api.shop.com"}


def test_sqli_xss():
    assert sol.find_user(ROWS, "' OR '1'='1") == []
    assert sol.find_user(ROWS, "a@x.com") == [("a@x.com",)]
    assert "<script>" not in sol.render("<script>alert(1)</script>hi")


def test_path_ssrf_shell():
    assert sol.safe_path("/tmp/base", "bill.pdf").name == "bill.pdf"
    with pytest.raises(ValueError):
        sol.safe_path("/tmp/base", "../../etc/passwd")
    assert sol.url_ok("https://api.shop.com/o", ALLOW)
    with pytest.raises(ValueError):
        sol.url_ok("http://169.254.169.254/x", ALLOW | {"169.254.169.254"})
    assert sol.run_echo("hello; rm -rf /") == "hello; rm -rf /"
