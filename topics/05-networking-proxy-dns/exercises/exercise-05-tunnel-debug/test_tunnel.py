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


sol = _load("sol05_ex05")


def test_tunnel():
    cmd = sol.tunnel("local", lport=5433, rhost="db.internal", rport=5432, via="bastion")
    assert cmd == "ssh -N -L 5433:db.internal:5432 bastion"
    assert "-D 1080" in sol.tunnel("socks", lport=1080, via="bastion")
    with pytest.raises(ValueError):
        sol.tunnel("local", lport=99999, rhost="x", rport=80, via="b")
    with pytest.raises(ValueError):
        sol.tunnel("local", lport=8080, rhost="a; evil", rport=80, via="b")


def test_diagnose():
    assert sol.diagnose("cert") == "openssl s_client"
    assert sol.diagnose("packets") == "tcpdump"
    assert len(sol.TOOLS) == 8
    assert sol.diagnose("weird") == "start with ping (cheap first)"
