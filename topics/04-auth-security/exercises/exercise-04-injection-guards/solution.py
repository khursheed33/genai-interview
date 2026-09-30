"""Solution: exact match, escape, cage, allowlist, argv-list."""

import html
import ipaddress
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def find_user(db_rows, email):
    return [r for r in db_rows if r[0] == email]  # binding = compare as DATA


def render(text):
    return html.escape(text)


def safe_path(base, name):
    p = (Path(base).resolve() / name).resolve()
    if Path(base).resolve() not in p.parents and p != Path(base).resolve():
        raise ValueError("traversal blocked")
    return p


def url_ok(url, allow):
    host = urlparse(url).hostname or ""
    if host not in allow:
        raise ValueError("host not allowlisted")
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None
    if ip is not None and (ip.is_private or ip.is_link_local or ip.is_loopback):
        raise ValueError("non-public IP blocked")
    return True


def run_echo(payload):
    out = subprocess.run(
        [sys.executable, "-c", "import sys; print(sys.argv[1])", payload],
        capture_output=True,
        text=True,
        shell=False,
    )
    return out.stdout.strip()
