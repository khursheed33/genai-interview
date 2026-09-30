# Interview Questions — Backend Frameworks

Say the **bold line** first, then the hook.

## Frameworks & lifecycle

- [ ] **[theory]** FastAPI vs Flask vs Django vs Express vs NestJS — pick for: GenAI API, tiny webhook, admin-heavy CRUD, big TS team?
  - **GenAI API → FastAPI (async+Pydantic+docs). Tiny webhook → Flask/Express. Admin-heavy → Django (admin+ORM day one). Big TS → NestJS (modules+DI).**
- [ ] **[theory]** Request lifecycle in any framework?
  - **Route → middleware (trace/auth/log) → validate (422 at gate) → DI → thin handler → serialize (response_model) → trace header out.**
- [ ] **[hands-on]** Where does validation live? Where does `password_hash` get stripped?
  - **Pydantic `Field` at the gate (auto-422); `response_model` without the secret on exit — never `if`-spaghetti or manual deletes.**

## Routing / DI / serialization

- [ ] **[hands-on]** Routers vs giant `main.py`? Path vs query params?
  - **Split `orders.py/users.py` + `include_router(prefix="/v1")`. Path = identity, query = options (limit/verbose).**
- [ ] **[theory]** `Depends` with `yield` — what runs when? Why `dependency_overrides`?
  - **Code before `yield` = setup, after = teardown (finally — even on error). Overrides swap DB/auth fakes in tests without touching routes.**
- [ ] **[hands-on]** Compose auth + db + pagination in one endpoint signature. Why cap limit?
  - **`def listing(db=Depends(get_db), user=Depends(get_user), p=Depends(pagination))`. Cap (`le=100`) at the gate — `?limit=1M` melts staging otherwise.**

## ORM / DB layer

- [ ] **[theory]** Engine vs Session vs migration? One Session per…?
  - **Engine = pooled road. Session = per-request basket (add→commit once, rollback on error, close always via DI). Migrations (Alembic) = reviewed renovation log, run as a job — never racing app startups.**
- [ ] **[hands-on]** N+1 demo + fix? How do you prove it?
  - **Loop `user.orders` with lazy select = 1+5 queries. Fix: `selectinload/joinedload` → 2. Prove with `before_cursor_execute` counter (see example: 6→2).**
- [ ] **[theory]** Repository buys you what? Duplicate email → which status?
  - **Hides SQL behind `OrderRepo.get/create` (fake in unit tests). `IntegrityError` → `409`, never 500.**
- [ ] **[theory]** Pool settings + `pool_pre_ping`? Sync ORM in `async def`?
  - **`pool_size + max_overflow`, PgBouncer in prod, `pre_ping` kills dead conns. Sync ORM blocks the loop — call from `def` endpoints (threadpool) or `run_in_executor`.**

## Async / servers / lifespan

- [ ] **[theory]** `async def` vs `def` endpoint — decide for: LLM stream, PIL resize, sync boto3 call?
  - **LLM stream → `async def` + `StreamingResponse` (awaits without blocking). PIL/boto3/sync-ORM → `def` (threadpool). Blocking call inside `async def` freezes ALL requests.**
- [ ] **[theory]** WSGI vs ASGI? Uvicorn vs Gunicorn-Uvicorn? Worker count?
  - **WSGI = sync-only (Flask/Django classic). ASGI = async+websockets+lifespan. Prod: Gunicorn manages processes + Uvicorn workers serve ASGI. `workers ≈ 2×CPU+1` (sync); fewer for async.**
- [ ] **[hands-on]** Lifespan does what? `/health` vs `/ready`?
  - **Opens pools/models ONCE (`yield` serves, close after). `/health` = alive (fast, no DB); `/ready` = warm (pool+migrations ok) for K8s probes.**

## Tasks / files / config

- [ ] **[scenario]** PDF summary takes 40s — design it (status codes included).
  - **`POST → save job row (pending) → enqueue id → 202 + Location: /jobs/77`. Worker: idempotent (`job_id` unique), 3–5 retries w/ backoff, DLQ + alert. Client polls or webhook.**
- [ ] **[theory]** `BackgroundTasks` vs Celery vs RQ vs BullMQ vs APScheduler?
  - **BackgroundTasks = post-response wipe only (dies with server!). Celery = serious Python queues (+beat scheduler). RQ/Dramatiq = simpler. BullMQ = Node/Redis. APScheduler = in-process crons (prod → beat/CronJob, never cron in 3 replicas).**
- [ ] **[hands-on]** Upload rules? 2 GB video — `.read()` it?
  - **Check type+size BEFORE reading, stream chunks to disk/S3, randomize names (no traversal), presigned S3 for big files (server never touched). Never `.read()` GBs into RAM.**
- [ ] **[hands-on]** Stream 50k rows / LLM tokens — how? Test it?
  - **Generator + `StreamingResponse` (NDJSON `application/x-ndjson` / SSE `text/event-stream`); O(1) memory. Test via TestClient reading lines.**
- [ ] **[theory]** 12-factor config in 30s + "prod secret missing"?
  - **One image, env decides; secrets from Vault (never git/bundle); fail fast at boot (`ValueError`); mask in logs (`sk-***`); logs to stdout.**

## Gotchas (say unprompted)

- `time.sleep`/`requests` inside `async def` = full-loop freeze under load.
- Missing `response_model` leaks `password_hash`; missing `le=100` invites `?limit=1M`.
- Shared Session across requests = cross-talk + pool exhaustion; `BackgroundTasks` for important jobs = lost on deploy.
- Filenames from users → path traversal; `SecretStr` + masked logging for keys.

## Self-score (0–5)

- Frameworks+lifecycle: __ / routing+DI: __ / ORM: __ / async+servers: __ / tasks: __ / files+config: __
- Whiteboard: Depends chain + N+1 fix + 202-job flow + lifespan? Y/N each.
