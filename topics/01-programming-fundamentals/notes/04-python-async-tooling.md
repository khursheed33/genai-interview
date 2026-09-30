# 04 — Python Async, GIL, Threads vs Processes + Tooling

## 1. One cook story (the only mental model you need)

- **Sync:** one cook makes 1 dosa at a time, stares at boiling milk (CPU idle during I/O). Slow.
- **`asyncio` (single cook, smart):** cook puts milk to boil, *while waiting* cuts veggies. One thread, many waiting tasks. Best for **I/O-bound**: API calls, DB, file, LLM calls.
- **Threads (many cooks, one stove):** many cooks but **GIL = one stove burner**. Good when cooks mostly wait (I/O). Bad when all need burner (CPU math) — they queue.
- **Processes (many kitchens):** each cook has own kitchen (own memory/GIL). Best for **CPU-bound**: image resize, embeddings math, JSON parsing of GBs. Cost: heavier, need pickle to share.

**GIL** = Global Interpreter Lock: only one thread runs Python bytecode at a time. NumPy/C extensions can release it. That's why `threading` doesn't speed pure-Python loops.

```python
import asyncio


async def call_llm(name, delay):
    print(f"{name} cooking...")
    await asyncio.sleep(delay)  # milk boiling — let others work
    return f"{name} done"


async def main():
    # both boil together — total ~1s, not 2s
    return await asyncio.gather(call_llm("a", 1), call_llm("b", 1))


asyncio.run(main())
```

Rules:
- `async def` + `await` only inside async. `await` = "wait here without blocking others".
- Never call blocking `time.sleeprequests.get` inside async — use `asyncio.sleep`, `httpx.AsyncClient`.
- CPU-bound? → `multiprocessing` / `ProcessPoolExecutor`. I/O-bound with blocking libs? → `ThreadPoolExecutor`.
- `asyncio.gather` (all together), `wait_for` (timeout), `Semaphore(10)` (don't DDoS provider).

FastAPI: `def` endpoint runs in threadpool, `async def` on event loop — mixing wrong blocks the loop.

## 2. venv / pip / uv — separate tiffins per project

System Python = school kitchen. Each project needs own tiffin (deps versions differ).

```
uv sync            # create .venv + install from pyproject/lock (fast, modern)
uv add pydantic    # add dep
uv run pytest      # run inside venv
```

Old: `python -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt`. `poetry` similar. `uv` replaces pip+venv (10-100x faster). Commit `pyproject.toml` + lock, never `.venv/`.

## 3. Exceptions + logging — fire alarm, not print()

```python
class PaymentFailed(Exception):  # custom = specific alarm, not generic shout
    pass


try:
    charge()
except PaymentFailed as e:
    logger.exception("charge failed for order %s", order_id)  # traceback!
    raise  # re-raise, don't swallow
else:
    dispatch()  # only if no fire
finally:
    release_seat()  # always clean
```

Logging > print: levels (`DEBUGINFO/WARNING/ERROR`), JSON in prod, correlation-id (`order_id=...`) so you trace one request across services. Never log PII/secrets.

## 4. Memory / GC / profiling — toy room cleaning

- Python counts references; when 0 → frees. **GC** handles cycles (a holds b holds a) via generations.
- `sys.getsizeof([1,2])` lies (shallow). Use `tracemalloc` / `memory_profiler` for real.
- Leaks in GenAI: global list caching embeddings, unbounded `lru_cache`, keeping LangChain messages forever. Fix: bounded cache, pagination, `del` + weakrefs.
- Profile: `python -m cProfile -s cumtime app.py`, `time.perf_counter` for latency, `tracemalloc` for memory.

**One-liners:** "Async for waiting, threads for blocking-I/O, processes for CPU." / "GIL: one bytecode at a time." / "One venv per project; log with context, raise specific exceptions."
