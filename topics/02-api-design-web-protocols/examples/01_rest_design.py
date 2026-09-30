"""01_rest_design.py — restaurant menu rules as code.

Run: uv run python topics/02-api-design-web-protocols/examples/01_rest_design.py
"""

# Safe = read-only. Idempotent = repeat N times, same effect as once.
METHODS = {
    "GET": {"safe": True, "idempotent": True},
    "HEAD": {"safe": True, "idempotent": True},
    "OPTIONS": {"safe": True, "idempotent": True},
    "PUT": {"safe": False, "idempotent": True},
    "DELETE": {"safe": False, "idempotent": True},
    "POST": {"safe": False, "idempotent": False},
    "PATCH": {"safe": False, "idempotent": False},  # *unless op is set-value
}

print("DELETE idempotent (effect=gone):", METHODS["DELETE"]["idempotent"])
assert METHODS["GET"]["safe"] and not METHODS["POST"]["idempotent"]


def check_route(method, path):
    """Tiny REST naming linter: nouns not verbs, plural collections."""
    bad_verbs = ("get", "create", "update", "delete", "fetch", "add", "post")
    verdicts = []
    low = path.lower()
    if any(f"/{v}" in low or low.endswith(f"/{v}") for v in bad_verbs):
        verdicts.append("verb-in-uri (use HTTP method instead)")
    if method == "GET" and low.rstrip("/").split("/")[-1].rstrip("s") == low.split("/")[-1]:
        pass  # keep simple: most collections should be plural
    return verdicts or ["ok"]


print("GOOD:", check_route("GET", "/orders/101"))
print("BAD :", check_route("GET", "/getOrder"))
assert check_route("GET", "/orders/101") == ["ok"]
assert check_route("GET", "/getOrder") != ["ok"]


def rmm_level(has_resources, uses_verbs_status, has_links):
    if not has_resources:
        return 0
    if not uses_verbs_status:
        return 1
    return 3 if has_links else 2


assert rmm_level(True, True, True) == 3
assert rmm_level(True, False, False) == 1
print("RMM swamp->glory:", [rmm_level(True, False, False), rmm_level(True, True, True)])
print("OK — nouns in URI, verbs in methods; PUT/DELETE repeat-safe, POST is not")
