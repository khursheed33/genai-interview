# 04 — Sync vs Async, ASGI vs WSGI, Servers & Lifespan

## 1. Sync vs async endpoints (one cook, revisited from topic 01)

```python
@app.get("/slow")
async def slow():
    return await call_llm()  # event loop: waits WITHOUT blocking others


@app.get("/calc")
def calc():
    return fib(35)  # threadpool: blocks a thread, loop stays free
```

- `async def` = runs ON the event loop. One blocking call (`time.sleep`, `requests.get`) freezes EVERYONE. Use `httpx.AsyncClient`, `asyncpg`, `await`.
- `def` = runs in a threadpool (default 40 threads). Safe for sync ORMs (`SQLAlchemy` sync, `boto3`) and CPU-ish work.
- Rule of thumb: **I/O with async libs → `async def`; sync libs/CPU → `def`.** Mixed wrong = outage under load (40 threads × 30s LLM call = dead).
- GenAI: stream tokens from `async def` + `StreamingResponse`; CPU embedding math → threadpool or separate worker.

## 2. WSGI vs ASGI = old phone line vs fiber

| | WSGI (Gunicorn + Flask/Django) | ASGI (Uvicorn + FastAPI/Starlette) |
|---|---|---|
| Style | sync only, one request per worker at a time | sync AND async, websockets, SSE, lifespan |
| Concurrency | more processes/threads | event loop (+ workers) |
| Use | classic Django/Flask | FastAPI, Django Channels, Starlette |

## 3. Running it (workers = extra counters)

```bash
uvicorn app:app --workers 4                    # dev / simple prod
gunicorn app:app -k uvicorn.workers.UvicornWorker -w 4   # prod: process manager + ASGI speed
```

- Formula: `workers ≈ 2×CPU + 1` for sync; fewer (per-core) for async (loop does the multiplexing). K8s HPA scales pods; workers scale inside the pod.
- Behind Nginx (static files, TLS, gzip) + health probes (`/health` → 200 fast, no DB query!). Graceful shutdown: finish in-flight (30s) before SIGKILL.

## 4. Lifespan = shop opening/closing ritual (replaces `@app.on_event`)

```python
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    app.state.pool = await open_pool()  # open once: DB pool, ML model, Redis
    yield  # ...serve traffic...
    await app.state.pool.close()  # close once: no leaks
```

Open heavy things ONCE (model weights, pools), never per request. Health vs readiness: `/health` (alive?) vs `/ready` (pool warm? migrations done?).

One-liner: **"Async for waiting, def for blocking libs; ASGI for modern; pools+models open once in lifespan."**
Runnable: lifespan + TestClient portal in `../examples/01_minimal_fastapi.py`.
