"""Solution: thin handlers over a dict store; guard + pack via Pydantic."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class OrderIn(BaseModel):
    email: str
    items: list[str] = Field(min_length=1)


class OrderOut(OrderIn):
    id: int


def build_app():
    app = FastAPI()
    app.state.db = {"orders": {}}

    @app.post("/orders", response_model=OrderOut, status_code=201)
    def create(o: OrderIn):
        db = app.state.db["orders"]
        oid = len(db) + 1
        db[oid] = o.model_dump()
        return {"id": oid, **o.model_dump()}

    @app.get("/orders/{oid}", response_model=OrderOut)
    def one(oid: int):
        try:
            return {"id": oid, **app.state.db["orders"][oid]}
        except KeyError:
            return JSONResponse({"title": f"order {oid} not found"}, status_code=404)

    return app
