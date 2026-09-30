"""01_minimal_fastapi.py — cafe with printed menu + guard + opening ritual.

Run: uv run python topics/03-backend-frameworks/examples/01_minimal_fastapi.py
Tests the app WITHOUT a server via TestClient (lifespan runs in the `with` block).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

OPENED = {"n": 0}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = {"orders": {}}  # open once: pool/model/redis in real life
    OPENED["n"] += 1
    yield
    app.state.db.clear()  # close once


class OrderIn(BaseModel):
    email: str
    items: list[str] = Field(min_length=1)


class OrderOut(OrderIn):
    id: int


app = FastAPI(lifespan=lifespan)


@app.post("/orders", response_model=OrderOut, status_code=201)
def create(o: OrderIn):
    db = app.state.db
    oid = len(db["orders"]) + 1
    db["orders"][oid] = o.model_dump()
    return {"id": oid, **o.model_dump()}


@app.get("/orders/{oid}", response_model=OrderOut)
def one(oid: int):
    return {"id": oid, **app.state.db["orders"][oid]}


with TestClient(app) as client:
    assert OPENED["n"] == 1  # lifespan ran
    r = client.post("/orders", json={"email": "a@x.com", "items": ["dosa"]})
    assert r.status_code == 201, r.text
    assert r.json()["id"] == 1
    assert client.get("/orders/1").json()["items"] == ["dosa"]
    bad = client.post("/orders", json={"email": "a@x.com", "items": []})
    assert bad.status_code == 422  # guard rejects at the gate, handler never ran
    print("POST 201 + Location-style id, GET 200, bad items -> 422")
print("OK — lifespan opens once, Pydantic guards, response_model packs gifts")
