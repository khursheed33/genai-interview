# 07 — Orchestration: Conductors (Airflow/Temporal/Prefect/Step Functions)

Queues move EVENTS; orchestrators run whole **plays** (retries, branches, human approvals, backfills!) durably.

## 1. The four (pick by durability needs!)

| Tool | Story | Superpower |
|---|---|---|
| **Airflow** | rehearsal schedule (DAGs on cron!) | sensors (wait for file/partition!), backfill years, huge operator library |
| **Temporal** | play that survives theater fire (durable execution!) | code RESUMES after crash (workflows as functions + activities + signals!) |
| **Prefect** | Airflow's sporty sibling | dynamic flows, easy local→cloud |
| **Step Functions** | AWS's state machine | visual JSON states + direct service integrations (no servers!) |

## 2. Rules (all four!)

- Tasks IDEMPOTENT + retryable (reruns happen — backfills, zombie recovers!). Deterministic workflow code (Temporal replays history — `random()`/`now()` via side-effect APIs!). Version workflows (running + new code coexist — Temporal versioning, Airflow `catchup=False` care!). Human gates as explicit steps (approval → signal, never Slack-and-pray!). Timeouts + heartbeat per task (stuck ≠ dead — detect both!). Secrets via vault (never in DAG code!).

## 3. GenAI plays (where this earns!)

Nightly **eval regression** (golden set → judge → alert on drift, topic 21!), **doc re-index** pipelines (parse→chunk→embed→upsert, topic 19!), **LLM batch** jobs (queue 10k prompts → rate-limited fan-out → DLQ, topic 23!). Scheduler triggers, workers execute (separation from topic 03's helpers — same religion, bigger church!).

Runnable DAG runner (topo order + retries + timing): `../examples/08_dag_runner.js`.
One-liner: **"Queues move facts, conductors run plays; idempotent tasks, versioned plays, humans as steps."**
