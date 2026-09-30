# 06 — Uploads, Streaming, Pagination: Tiffin In, Conveyor Out

## 1. File uploads = tiffin inspection at the gate

```python
@app.post("/docs", status_code=201)
async def upload(file: UploadFile):  # multipart/form-data
    assert file.content_type == "application/pdf"
    assert file.size and file.size < 50_000_000  # 50 MB cap — check BEFORE reading!
    # stream to disk/S3 in chunks — never .read() a 2 GB video into RAM
    with open(f"/tmp/{file.filename}", "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)
    return {"name": file.filename}
```

Rules: content-type + extension + size checks, randomize stored names (`uuid.pdf` — no `../../etc` traversal!), scan (ClamAV) if user-facing, hand big files to presigned S3 URLs (browser uploads direct, server never touched). Direct-to-S3 = 10× cheaper.

## 2. Streaming = conveyor, not warehouse (`StreamingResponse`)

```python
from fastapi.responses import StreamingResponse


@app.get("/export")  # NDJSON: one JSON per line
def export():
    def rows():
        for o in stream_orders():  # generator — O(1) memory
            yield o.model_dump_json() + "\n"

    return StreamingResponse(rows(), media_type="application/x-ndjson")


@app.get("/chat")  # LLM tokens as SSE
async def chat():
    async def tokens():
        async for t in llm.astream("hi"):
            yield f"data: {t}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(tokens(), media_type="text/event-stream")
```

Same for file downloads (`FileResponse` + `Content-Disposition: attachment`). Test by iterating `client.stream(...)` — see `../examples/05_upload_stream_page.py`.

## 3. Pagination as a reusable dependency (write once!)

```python
from fastapi import Query


def pagination(limit: int = Query(20, le=100), offset: int = Query(0, ge=0)):
    return {"limit": limit, "offset": offset}


@app.get("/orders")
def listing(p=Depends(pagination), db=Depends(get_db)):
    return db.query(Order).offset(p["offset"]).limit(p["limit"]).all()
```

`le=100` caps abuse at the gate. Cursor variant for feeds (topic 02): `after_id` + `WHERE id > after`. Always envelope `{data, total/pageInfo}` so frontends stop guessing.

One-liner: **"Uploads: validate, cap, stream to S3. Downloads/LLM: stream via generators. Pages: capped dep, enveloped."**
