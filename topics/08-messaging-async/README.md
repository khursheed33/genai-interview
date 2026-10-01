# 08 - Messaging and Async Processing

> Scope: README.md section 8: queues vs streams, Kafka/RabbitMQ/SQS/SNS/PubSub, delivery semantics, idempotent consumers/DLQ, EDA/CQRS/saga/outbox, Airflow/Temporal
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- Patterns → `notes/01-queues-streams.md` (compete/broadcast/replay, managed map, backpressure)
- Kafka → `notes/02-kafka.md` (partitions/groups/offsets, retention/compaction, EOS, ops)
- RabbitMQ → `notes/03-rabbitmq.md` (4 exchanges, acks, prefetch, quorum, delayed)
- Semantics → `notes/04-semantics.md` (3 promises, idempotency, DLQ, ordering)
- EDA → `notes/05-eda-patterns.md` (sourcing/CQRS/saga/outbox)
- Processing → `notes/06-processing.md` (batch/stream/Kappa, windows, Spark/Flink kit)
- Conductors → `notes/07-orchestration.md` (Airflow/Temporal/Prefect/Step Functions + GenAI plays)

## Examples (8 runnable — verified)
| File | Covers | Run |
|---|---|---|
| `examples/01_queue_vs_stream.py` | queue/pubsub/log promises | `uv run python topics/08-messaging-async/examples/01_queue_vs_stream.py` |
| `examples/02_kafka_sim.py` | key→partition, rebalance, offsets, compact | same pattern |
| `examples/03_rabbitmq_sim.py` | 3 exchanges, ack/prefetch | same pattern |
| `examples/04_semantics_dlq.py` | 3 semantics, DLQ, backpressure | same pattern |
| `examples/05_saga_outbox.py` | outbox relay + saga compensate | same pattern |
| `examples/06_redis_streams.py` | XADD/groups/ACK/PEL (fakeredis) | same pattern |
| `examples/07_sourcing_cqrs.py` | fold/snapshot/time-travel/project | same pattern |
| `examples/08_dag_runner.js` | topo + retries + timing | `node .../08_dag_runner.js` |

## Exercises (5 — `uv run pytest topics/08-messaging-async/exercises -q`, 9 tests)
- `exercise-01-partitions` — stable hash + fair deal
- `exercise-02-topic-route` — `*`/`#` incl. mid-`#`
- `exercise-03-idempotent-dlq` — dedupe + park poison
- `exercise-04-saga` — reverse compensation order
- `exercise-05-sourced-account` — fold/snapshot/time-travel

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
- [x] Notes drafted (7 files, post-office/diary/conductor stories)
- [x] Examples run (8 files, verified: sims + fakeredis + node)
- [x] Exercises done (5 exercises, 9 pytest tests green)
- [x] Interview Qs revised (20+ Q/A in `interview-questions.md`)
