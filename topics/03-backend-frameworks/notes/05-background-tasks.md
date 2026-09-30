# 05 — Background Tasks: Kitchen Helpers (Celery, RQ, BullMQ…)

HTTP must answer FAST (<1s). Slow cooking (PDF parse, embeddings, emails, SMS) goes to helpers behind a queue.

## 1. The pattern (same in every tool)

```
request → validate → SAVE job row (pending) → enqueue {job_id} → return 202 + Location: /jobs/77
worker: dequeue → run with retries → update job row (done/failed) → notify (webhook/SSE)
client: poll GET /jobs/77 or listen for webhook
```

Return `202` instantly; never hold HTTP open 60s. Job row in DB = truth (survives restarts); queue = delivery van.

## 2. Pick your helper

| Tool | Story | Use |
|---|---|---|
| FastAPI `BackgroundTasks` | Waiter wipes table after you leave | tiny post-response work (log, single email). Dies with server — NOT for important jobs! |
| **Celery** (+Redis/RabbitMQ) | Full catering company: retries, beat scheduler, canvas | Python standard for serious queues |
| **RQ / Dramatiq** | Food truck (simple) | small Python teams, fewer moving parts |
| **BullMQ** (Node/Redis) | Node catering | NestJS/Express stacks |
| **APScheduler** | Wall clock + alarm | in-process crons (reports, cleanup). For prod crons prefer Celery beat / K8s CronJob |

## 3. Rules that save careers

- **Idempotent jobs**: same `job_id` twice = one effect (`processed_ids` set / DB unique key). Retries WILL duplicate — design for it!
- **Retries**: 3–5×, exponential backoff + jitter (topic 02!), poison → DLQ + alert (don't clog the queue).
- **Timeouts per job** (300s default killer), **ack late** (only after success, else redelivered), **small payloads** (pass IDs, not 50 MB files — worker re-fetches).
- **Priority lanes**: `llm-gpu` queue ≠ `email` queue (bulkhead again!). Monitor depth + age (Grafana alert: 1000 stuck >5 min).
- Scheduler: `beat`/`CronJob` enqueues; workers execute. Never cron-inside-app-replicas (3 pods = 3 emails!).

```python
# FastAPI tiny version (learning only!)
@app.post("/summarize", status_code=202)
def start(doc: DocIn, bg: BackgroundTasks):
    jid = save_job("pending")
    bg.add_task(slow_summarize, jid, doc.text)  # runs AFTER response sent
    return {"job_id": jid, "status_url": f"/jobs/{jid}"}
```

One-liner: **"202 + job row + queue; idempotent + retried + DLQ'd; payloads carry IDs, not files."**
Runnable queue-with-retry demo: `../examples/04_tasks_queue.py`.
