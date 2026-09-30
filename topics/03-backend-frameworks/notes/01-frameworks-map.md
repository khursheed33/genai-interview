# 01 — Frameworks Map: Dhabas, Cafes & Food Courts

Every backend framework is a restaurant. Same hungry customers (HTTP), different kitchens.

## 1. The Python kitchens

| Framework | Story | Reach for it when… | Watch out |
|---|---|---|---|
| **FastAPI** | Modern cafe: printed menu (OpenAPI) + fast waiter (async) + strict guard (Pydantic) | APIs, GenAI services, SSE/streaming, teams wanting docs+validation free | Magic hides complexity (Depends); sync-blocking inside `async def` freezes loop |
| **Flask** | Home dhaba: one kadhai, you bring spices | tiny services, webhooks, learning HTTP | No async/validation/DI built-in — you assemble everything |
| **Django / DRF** | Food court with admin office, security, billing | CRUD-heavy products, admin panel, auth, ORM+migrations on day one | Heavy; async still second-class; overkill for one endpoint |

## 2. The Node kitchens

| Framework | Story | Reach for it when… |
|---|---|---|
| **Express** | Street cart: 5 lines and you're serving | prototypes, gateways/BFF, middleware chains |
| **NestJS** | Five-star hotel: uniform, DI, modules, decorators | large TS teams wanting Angular-style structure (controllers/services/modules) |

Same ideas everywhere: **route → parse → validate → handle → serialize**. Only the uniforms differ:
FastAPI `Depends()` = NestJS constructor injection = Express `app.use(auth)` = Django middleware + DRF serializers.

## 3. Request lifecycle (works in ALL of them)

```
TCP → routing (/orders/{id} matches?) → middleware (trace/auth/log)
→ validation (Pydantic/DTO — 422 here, not in business code!)
→ DI (give me db, current_user) → handler (business logic)
→ serialize (response_model hides password!) → middleware-out (trace header)
```

Golden rules: validate at the GATE (return `422` before touching DB), serialize on EXIT (never leak `password_hash`), keep handlers thin (call a service/repo you can unit-test without HTTP).

## 4. FastAPI in 20 lines (taste it)

```python
from fastapi import Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()


class OrderIn(BaseModel):
    items: list[str]


class OrderOut(OrderIn):
    id: int


def get_db():
    yield {"orders": {}}  # DI: real DB in prod, fake in tests


@app.post("/orders", response_model=OrderOut, status_code=201)
def create(o: OrderIn, db=Depends(get_db)):
    oid = len(db["orders"]) + 1
    db["orders"][oid] = o.model_dump()
    return {"id": oid, **o.model_dump()}
```

Run it: `uv run uvicorn` comes later (`04-async-sync-asgi.md`); test it WITHOUT a server via `TestClient` — see `../examples/01_minimal_fastapi.py`.

One-liners: **"FastAPI for APIs+GenAI, Flask for tiny, Django for admin-heavy, Express for quick Node, NestJS for big TS." / "Validate in, serialize out, thin handlers."**
