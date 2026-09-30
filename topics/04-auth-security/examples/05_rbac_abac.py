"""05_rbac_abac.py — badges, rulebook + the IDOR guard (OWASP API #1).

Run: uv run python topics/04-auth-security/examples/05_rbac_abac.py
"""

ROLES = {"viewer": 1, "editor": 2, "manager": 3, "admin": 4}
ORDERS = {7: {"user_id": "asha", "region": "blr", "amount": 5000}}


def require_role(user_roles, *allowed):
    if not set(user_roles) & set(allowed):
        raise PermissionError(f"needs one of {allowed}")
    return True


assert require_role(["manager"], "manager", "admin")
try:
    require_role(["viewer"], "admin")
    raise AssertionError("viewer entered admin room?!")
except PermissionError:
    print("RBAC: viewer blocked from admin action")


def may_refund(user, order, hour):
    return (
        user["role"] in ("manager", "admin")
        and order["region"] == user["region"]
        and order["amount"] <= 10_000
        and 9 <= hour < 18
    )


mgr = {"role": "manager", "region": "blr"}
assert may_refund(mgr, ORDERS[7], 12)
assert not may_refund(mgr, ORDERS[7], 22)  # after hours? no
assert not may_refund({"role": "manager", "region": "del"}, ORDERS[7], 12)  # wrong region? no
print("ABAC: region+amount+hours all checked")


def get_order(current, oid):
    order = ORDERS.get(oid)
    if order is None:
        return 404, None
    # OBJECT-level check: owner OR admin — every read, no exceptions!
    if order["user_id"] != current["id"] and "admin" not in current["roles"]:
        return 403, None
    return 200, order


assert get_order({"id": "asha", "roles": ["user"]}, 7)[0] == 200
assert get_order({"id": "bob", "roles": ["user"]}, 7)[0] == 403  # bob can't read asha's!
assert get_order({"id": "root", "roles": ["admin"]}, 7)[0] == 200
print("OK — RBAC on routes, ABAC for context, owner-or-role on EVERY object")
