"""05_upload_stream_page.py — tiffin in, conveyor out (FastAPI).

Run: uv run python topics/03-backend-frameworks/examples/05_upload_stream_page.py
Covers: size-capped upload (streamed), NDJSON StreamingResponse, capped pagination dep.
"""

from fastapi import Depends, FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()
ORDERS = [{"id": i, "item": "dosa"} for i in range(1, 51)]


class DocOut(BaseModel):
    name: str
    size: int


@app.post("/docs", response_model=DocOut, status_code=201)
async def upload(file: UploadFile):
    assert file.content_type == "application/pdf", "only pdf"
    size = 0
    while chunk := await file.read(1024 * 64):  # stream — never whole file in RAM
        size += len(chunk)
        assert size < 5_000_000, "too big (5 MB cap)"
    return {"name": file.filename or "unnamed", "size": size}


def pagination(limit: int = 20, offset: int = 0):
    return {"limit": min(limit, 100), "offset": max(offset, 0)}


@app.get("/orders")
def listing(p=Depends(pagination)):
    return {"data": ORDERS[p["offset"] : p["offset"] + p["limit"]], "total": len(ORDERS)}


@app.get("/export")
def export():
    def rows():
        for o in ORDERS:  # generator — O(1) memory for 50k rows
            yield f'{{"id": {o["id"]}}}\n'

    return StreamingResponse(rows(), media_type="application/x-ndjson")


c = TestClient(app)
up = c.post("/docs", files={"file": ("bill.pdf", b"%PDF-fake-bytes", "application/pdf")})
assert up.status_code == 201 and up.json()["size"] > 0, up.text
p1 = c.get("/orders?limit=5&offset=10").json()
assert [o["id"] for o in p1["data"]] == [11, 12, 13, 14, 15] and p1["total"] == 50
exp = c.get("/export")
assert exp.headers["content-type"].startswith("application/x-ndjson")
assert exp.text.count("\n") == 50
print("upload 201, page ids 11-15, NDJSON lines:", exp.text.count("\n"))
print("OK — cap+stream uploads, capped page dep, generator streams")
