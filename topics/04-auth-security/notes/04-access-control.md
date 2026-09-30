# 04 — Access Control: Class Monitor, Rulebook & Bouncer (RBAC/ABAC/ACL)

## 1. The three rulebooks

| Model | Story | Example | Fits |
|---|---|---|---|
| **ACL** | Name on each door ("Asha may enter L3") | S3 bucket policy, file perms | single resources |
| **RBAC** | Badges: `cashier`, `manager`, `admin` — doors check badges | `DELETE /users` needs `admin` | most products (start here!) |
| **ABAC** | Rulebook: "managers may refund OWN-region orders < ₹10k in work hours" | attributes: role+dept+owner+amount+time | banks, multi-tenant SaaS |
| (ReBAC: Google-Zanzibar "viewer of parent folder inherits" — Drive-like; OPA/OPAL or SpiceDB when you outgrow ifs) |

## 2. RBAC done right (roles ≠ identities)

```
roles: viewer < editor < manager < admin      (hierarchy, least privilege)
permissions attach to ROLES, users get ROLES  (never user→permission spaghetti)
GET  /orders       → roles: *
POST /refunds      → roles: manager, admin
DELETE /users/{id} → roles: admin  (+ NOT self: admin can't delete own account!)
```

Enforce in ONE dep (`require_roles("admin")`), test the matrix (every role × every route — see `../examples/05_rbac_abac.py`). Frontend hides buttons; BACKEND rejects (curl doesn't care about your CSS!).

## 3. ABAC policy = tiny judge function (OPA when big)

```python
def may_refund(u, order, now):
    return (
        u.role in ("manager", "admin")
        and order.region == u.region
        and order.amount <= 10_000
        and 9 <= now.hour < 18
    )
```

Real OPA: same logic in Rego, sidecar/central, versioned like code, audited per decision. Graduate to OPA when: >2 services duplicate rules, auditors ask "who decided?", or tenants bring custom rules.

## 4. IDOR guard (the #1 API bug — OWASP API #1!)

```python
# BROKEN: any logged-in user fetches ANY order
order = db.get(Order, oid)

# FIXED: owner OR privileged role, checked on the OBJECT (not just the route!)
order = db.get(Order, oid)
if order.user_id != current.id and "admin" not in current.roles:
    raise HTTPException(403)
```

Rule: **authZ on the object, every time** (list endpoints filter `WHERE user_id = me` for non-admins). Tests: user-A can't GET user-B's `/orders/7` (403, not 404-leak!), admin can. Mass assignment too: strip `role: admin` from request bodies (allowlist fields!).

One-liner: **"RBAC badges on routes, ABAC rulebook for context, object-level check every read/write — tests per role × route."**
