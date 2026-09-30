"""09_openapi_contract.py — menu card printed before cooking.

Run: uv run python topics/02-api-design-web-protocols/examples/09_openapi_contract.py
"""

SPEC = {
    "openapi": "3.1.0",
    "paths": {
        "/orders/{id}": {
            "get": {
                "parameters": [{"name": "id", "in": "path", "required": True}],
                "responses": {"200": {"description": "ok"}, "404": {"description": "missing"}},
            }
        }
    },
}


def lint(spec):
    problems = []
    if not spec.get("openapi", "").startswith("3."):
        problems.append("openapi version must be 3.x")
    for path, ops in spec.get("paths", {}).items():
        for method, op in ops.items():
            for p in op.get("parameters", []):
                if p.get("in") == "path" and not p.get("required"):
                    problems.append(f"{method} {path}: path param must be required")
            if "responses" not in op:
                problems.append(f"{method} {path}: responses missing")
    return problems


def curl_get(base, path, token="TOKEN"):
    return f'curl -H "Authorization: Bearer {token}" {base}{path}'


assert lint(SPEC) == []
bad = {"openapi": "2.0", "paths": {"/x": {"get": {}}}}
assert len(lint(bad)) == 2
print(curl_get("https://api.shop.com", "/orders/101"))
print("OK — lint OpenAPI in CI, mock with Prism, gen SDKs, test with schemathesis")
