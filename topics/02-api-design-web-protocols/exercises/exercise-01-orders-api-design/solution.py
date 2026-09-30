"""Solution: nouns in URI, verbs in methods, right status per action."""

STATUS = {"create": 201, "ok": 200, "no_content": 204}

ROUTES = [
    {"method": "POST", "path": "/orders", "status": STATUS["create"]},
    {"method": "GET", "path": "/orders/{id}", "status": STATUS["ok"]},
    {"method": "GET", "path": "/orders", "status": STATUS["ok"]},
    {"method": "PUT", "path": "/orders/{id}", "status": STATUS["ok"]},
    {"method": "PATCH", "path": "/orders/{id}", "status": STATUS["ok"]},
    {"method": "DELETE", "path": "/orders/{id}", "status": STATUS["no_content"]},
]
