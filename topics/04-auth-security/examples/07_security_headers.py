"""07_security_headers.py — walls + masked audit trail.

Run: uv run python topics/04-auth-security/examples/07_security_headers.py
"""

import re

HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self'; "
    "frame-ancestors 'none'; object-src 'none'",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}
assert "frame-ancestors 'none'" in HEADERS["Content-Security-Policy"]
print("headers: HSTS + CSP + anti-frame + nosniff ready")


def cookie(name, val):
    return f"{name}={val}; HttpOnly; Secure; SameSite=Lax; Max-Age=3600; Path=/"


assert "HttpOnly" in cookie("session", "abc")


def mask_email(e):
    user, _, dom = e.partition("@")
    return (user[:1] + "***@" + dom) if dom else "***"


def mask_card(n):
    digits = re.sub(r"\D", "", n)
    return "****" + digits[-4:] if len(digits) >= 4 else "****"


assert mask_email("asha@x.com") == "a***@x.com"
assert mask_card("4111 1111 1111 1234") == "****1234"


def audit(actor, action, obj, meta):
    safe = {
        k: (mask_email(v) if "email" in k else mask_card(v) if "card" in k else v)
        for k, v in meta.items()
    }
    return {"actor": actor, "action": action, "object": obj, "meta": safe}


rec = audit("asha", "refund", "order:7", {"email": "asha@x.com", "card": "4111111111111234"})
assert rec["meta"] == {"email": "a***@x.com", "card": "****1234"}, rec
print("audit:", rec)
print("OK — headers on every response; PII masked before it hits the log")
