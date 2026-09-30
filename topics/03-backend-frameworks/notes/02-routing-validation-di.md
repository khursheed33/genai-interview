# 02 — Routing, Validation, Serialization, DI: Counter, Guard & Tiffin Delivery

## 1. Routing = shop counter signs (`/orders/{id}?verbose=true`)

```python
@app.get("/orders/{order_id}")                       # path param: identity
def one(order_id: int, verbose: bool = False): ...   # query param: options
@app.post("/orders", status_code=201)                # collection + verb = action
```

Rules: nouns (from topic 02), `/orders/{id}/items` ≤2 deep, trailing-slash consistent, version prefix (`/v1`) at router level: `app.include_router(r, prefix="/v1")`. Routers split files (`orders.py`, `users.py`) — one giant `main.py` rots by week 3.

## 2. Validation = strict guard (Pydantic v2)

```python
from pydantic import BaseModel, Field


class OrderIn(BaseModel):
    email: str
    items: list[str] = Field(min_length=1)
    coupon: str | None = Field(default=None, pattern=r"^[A-Z0-9]{6}$")
```

Bad JSON → automatic `422` with per-field errors (no `if` spaghetti!). `Field(gt=0, max_length=...)`, `EmailStr` (needs `email-validator`), nested models, `model_dump()` out / `model_validate()` in. Same models validate LLM structured output later (topic 16) — learn once, reuse everywhere.

## 3. Serialization = gift packing on exit (`response_model`)

```python
class UserOut(BaseModel):
    id: int
    name: str
    # password_hash deliberately ABSENT — can never leak


@app.get("/users/{uid}", response_model=UserOut)
def get_user(uid: int):
    return db_row  # extra keys stripped automatically
```

`response_model_exclude_unset`, `by_alias` (snake↔camel for JS frontends). Interview trap: "user sees password_hash" → missing response model.

## 4. DI = tiffin delivered, not cooked (`Depends`)

```python
def get_db():  # production tiffin
    db = SessionLocal()
    try:
        yield db  # setup...
    finally:
        db.close()  # ...teardown (even on error!)


def get_current_user(token=...): ...  # reusable auth slice


@app.get("/orders", response_model=list[OrderOut])
def listing(
    db=Depends(get_db), user=Depends(get_current_user), page=Depends(pagination)
): ...  # compose small deps!
```

Why: handlers stay pure (easy tests), resources always closed (`yield` finally), auth written once. **Testing superpower**: `app.dependency_overrides[get_db] = fake_db` — swap the kitchen without touching routes (see `../examples/02_di_overrides.py`).

Sub-deps, `yield` deps (setup/teardown), `use_cache=False` for per-request fresh (request-id!). NestJS constructors and Express `req.db = ...` middleware are the same idea in different uniforms.

One-liners: **"Validate in (422 at gate), serialize out (response_model), inject everything (overridable in tests)."**
