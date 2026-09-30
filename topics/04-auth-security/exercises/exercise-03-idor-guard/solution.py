"""Solution: object-level check every read; ABAC rule as one function."""

ORDERS = {
    7: {"owner": "asha", "region": "blr", "amount": 5000},
    8: {"owner": "bob", "region": "del", "amount": 50_000},
}


def authorize(current, oid):
    order = ORDERS.get(oid)
    if order is None:
        return 404, None
    if order["owner"] != current["id"] and "admin" not in current.get("roles", []):
        return 403, None
    return 200, order


def may_refund(user, order, hour):
    return (
        user.get("role") in ("manager", "admin")
        and order["region"] == user.get("region")
        and order["amount"] <= 10_000
        and 9 <= hour < 18
    )
