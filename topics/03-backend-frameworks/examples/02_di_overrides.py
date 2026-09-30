"""02_di_overrides.py — tiffin delivered; swap kitchen in tests.

Run: uv run python topics/03-backend-frameworks/examples/02_di_overrides.py
"""

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.testclient import TestClient


def get_db():
    db = {"orders": [{"id": 1}]}
    try:
        yield db  # setup...
    finally:
        db.clear()  # ...teardown, even on error


def get_user(authorization: str = Header(default="")):
    if authorization != "Bearer good":
        raise HTTPException(401, "who are you? login!")
    return {"name": "asha"}


def pagination(limit: int = 20, offset: int = 0):
    return {"limit": min(limit, 100), "offset": max(offset, 0)}  # cap at gate


app = FastAPI()


@app.get("/orders")
def listing(db=Depends(get_db), user=Depends(get_user), p=Depends(pagination)):
    return {"user": user["name"], "data": db["orders"][p["offset"] : p["offset"] + p["limit"]]}


client = TestClient(app)
assert client.get("/orders").status_code == 401  # no badge, no entry
ok = client.get("/orders", headers={"Authorization": "Bearer good"})
assert ok.json()["user"] == "asha"

# Swap the kitchen: fake DB, same routes
app.dependency_overrides[get_db] = lambda: {"orders": [{"id": 9}]}
swapped = client.get("/orders", headers={"Authorization": "Bearer good"})
assert swapped.json()["data"] == [{"id": 9}]
app.dependency_overrides.clear()
print("OK — Depends composes (db+user+page); overrides swap infra in tests")
