# 03 - Backend Frameworks

> Scope: README.md section 3: FastAPI/Flask/Django, Express/NestJS, ORM, background tasks, ASGI vs WSGI, config/12-factor
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- Map → `notes/01-frameworks-map.md` (FastAPI/Flask/Django/Express/NestJS picker + lifecycle)
- Routes → `notes/02-routing-validation-di.md` (routing, Pydantic guard, response_model, Depends)
- ORM → `notes/03-orm.md` (Session/basket, N+1 kill, migrations, repository)
- Async → `notes/04-async-asgi-servers.md` (def vs async def, WSGI/ASGI, workers, lifespan)
- Tasks → `notes/05-background-tasks.md` (202+jobs, Celery/RQ/BullMQ, idempotent+DLQ)
- Files → `notes/06-upload-stream-page.md` (capped uploads, StreamingResponse, page dep)
- Config → `notes/07-config-12factor.md` (env decides, vaults, fail fast, stdout logs)

## Examples (7 runnable — verified, real FastAPI + SQLAlchemy)
| File | Covers | Run |
|---|---|---|
| `examples/01_minimal_fastapi.py` | lifespan, 201/422, TestClient (no server!) | `uv run python topics/03-backend-frameworks/examples/01_minimal_fastapi.py` |
| `examples/02_di_overrides.py` | db+user+page deps, `dependency_overrides` | same pattern |
| `examples/03_sqlalchemy_nplus1.py` | N+1 counter 6→2 via `selectinload`, repo | same pattern |
| `examples/04_tasks_queue.py` | 202 + idempotent worker + retry + DLQ (stdlib) | same pattern |
| `examples/05_upload_stream_page.py` | capped upload, NDJSON stream, page dep | same pattern |
| `examples/06_config.py` | env decides, prod fail-fast, masked secrets | same pattern |
| `examples/07_node_http_api.js` | Express-style onion on bare `node:http` | `node .../07_node_http_api.js` |

## Exercises (5 — `uv run pytest topics/03-backend-frameworks/exercises -q`, 10 tests)
- `exercise-01-crud-api` — FastAPI CRUD + 201/404/422 via TestClient
- `exercise-02-pagination-dep` — clamp + slice bouncer
- `exercise-03-repo-n1` — repo + eager ≤2 queries + 409 mapping
- `exercise-04-job-retry` — retry counts + idempotency + DLQ
- `exercise-05-config-stream` — prod fail-fast + masked + lazy NDJSON

## Structure
- `README.md` - this checklist entry point
- `notes/` - your condensed notes (add `.md` per sub-topic)
- `examples/` - runnable minimal examples (python/js/sh)
- `exercises/` - practice tasks + solutions
- `interview-questions.md` - Q and A bank

## How to use
1. Read the checklist item in root README.
2. Add notes + code + diagrams here.
3. Do 2-3 exercises and 1 mini-project link in `projects/` if applicable.
4. Self-quiz with interview questions.

## Resources
- Add links as you learn (docs, papers, videos).
- Prefer primary sources: official docs, RFCs, papers.

## Progress
- [x] Notes drafted (7 files, dhaba/cafe/librarian stories)
- [x] Examples run (7 files, verified: TestClient + sqlite + node)
- [x] Exercises done (5 exercises, 10 pytest tests green)
- [x] Interview Qs revised (20+ Q/A in `interview-questions.md`)
