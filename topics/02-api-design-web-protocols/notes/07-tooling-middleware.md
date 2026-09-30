# 07 — Tooling & Middleware: Menu Printing + Kitchen Conveyor

## 1. Contracts first: OpenAPI / AsyncAPI (menu card printed BEFORE cooking)

```yaml
# openapi.yaml (snippet)
openapi: 3.1.0
paths:
  /orders/{id}:
    get:
      parameters: [{name: id, in: path, required: true, schema: {type: integer}}]
      responses: {'200': {description: ok}, '404': {$ref: '#/components/responses/NotFound'}}
```

- **OpenAPI/Swagger**: REST contract → interactive docs (Swagger UI), mock servers (Prism), SDK gen (OpenAPI Generator), contract tests (schemathesis). Single source of truth — review the YAML in PRs like code!
- **AsyncAPI**: same idea for events/WebSockets/Kafka (`channels: orderCreated: subscribe: ...`). Your `orderDelivered` webhook deserves a contract too.
- Flow: design YAML → mock → frontend builds parallel → implement → CI validates responses match schema. Mock servers unblock mobile teams for 2 weeks.

## 2. Daily tools (learn the keystrokes!)

```bash
curl -s -D - -o /dev/null -w " %{http_code} %{time_total}s\n" https://api.shop.com/orders/101
curl -X POST api.shop.com/orders -H "Content-Type: application/json" -d '{"items":["dosa"]}'
curl -v https://api...          # TLS + headers debug (see 05-networking topic later)
http POST api.shop.com/orders items:='["dosa"]' Authorization:"Bearer $T"   # HTTPie: human curl
```

Postman/Insomnia: collections + environments (`{{baseUrl}}`, `{{token}}`) → share → Newman runs them in CI as API tests.

## 3. Gateways = mall entrance (one door, many shops)

Kong / Apigee / AWS API GW / Azure APIM / Cloudflare: auth, rate limits, quotas, caching, version routing (`/v1→svc-a`), request shaping, retries, analytics, monetization. BFF (Backend-for-Frontend): separate thin gateway per client (mobile needs small payloads, web needs rich) — no more `?fields=` hacks everywhere.

## 4. Middleware / interceptors = conveyor-belt chefs

Every request passes chefs in ORDER: `correlation-id → auth → logging → validation → handler → error-mapper`. Order matters (auth before billable work!).

```python
# same idea in FastAPI, Express, Axios — onion model
async def middleware(request, call_next):
    request.id = request.headers.get("X-Request-ID", new_id())  # trace!
    try:
        return await call_next(request)  # next chef
    except KnownError as e:
        return problem_json(e)  # map to RFC7807
```

- **Axios interceptors**: attach token + `X-Request-ID` on request; refresh-on-401 + retry once on response.
- **Uses**: auth, structured logs (`method path status latency traceId`), retries, error→Problem mapping, correlation IDs, metrics. Guards (can I enter?) / pipes (transform?) / filters (which route?) are framework names for the same belt.
- Golden rule: middleware does cross-cutting ONLY — no business logic (that lives in handlers/services, testable without HTTP).

Runnable: `../examples/08_middleware.py` (onion chain with auth+trace+timing) + `../examples/09_openapi_contract.py` (spec lint + curl gen).
