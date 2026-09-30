"""Solution: secure defaults + mask-before-log."""

import re


def headers():
    return {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'; "
        "frame-ancestors 'none'; object-src 'none'",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
    }


def mask_email(e):
    user, _, dom = e.partition("@")
    return (user[:1] + "***@" + dom) if dom else "***"


def mask_card(n):
    digits = re.sub(r"\D", "", n)
    return "****" + digits[-4:] if len(digits) >= 4 else "****"


def audit(actor, action, obj, meta):
    safe = {
        k: (mask_email(v) if "email" in k else mask_card(v) if "card" in k else v)
        for k, v in meta.items()
    }
    return {"actor": actor, "action": action, "object": obj, "meta": safe}
