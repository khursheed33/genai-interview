# 01 — Queues vs Streams vs Pub/Sub: Post Office, Library & Loudspeaker

Three buildings, three promises. Pick by asking: **compete, broadcast, or replay?**

## 1. The three (memorize!)

| Pattern | Story | Promise | Examples |
|---|---|---|---|
| **Queue** (point-to-point) | post office counter: ONE clerk takes each parcel | each message → exactly ONE consumer (competing!) | SQS, RabbitMQ queue, Celery (topic 03!) |
| **Pub/Sub** (broadcast) | loudspeaker: EVERY room hears | each message → ALL subscribers (no replay for late joiners!) | SNS, Redis Pub/Sub, Google Pub/Sub |
| **Event log/stream** (diary) | library ledger: appended, numbered, re-readable | ordered durable log + offsets (replay from #42 anytime!) | Kafka, Redpanda, NATS JetStream, Redis Streams |

- Queue = distribute WORK (10 workers share 1M emails). Pub/Sub = notify MANY (order-paid → warehouse + email + fraud, all get it). Log = remember EVERYTHING (replay new service from day zero, audit, event sourcing — note 05!).
- Managed map: **SQS** (queue, at-least-once, DLQ native) + **SNS** (fan-out to SQS/HTTP!) = pub/sub-to-queues (best of both!); **EventBridge** (event bus + rules/filter → targets, SaaS events!); **Service Bus** (queues + topics/subs, sessions for ordering!); **NATS** (lightning subject-routing, JetStream adds persistence!); **Redis Streams** (Kafka-lite with groups — runnable in `../examples/06_redis_streams.py`).

## 2. Backpressure (flood control — everywhere!)

Producer floods, consumer sips → unbounded buffer = OOM. Shields: **bounded queues** (block / drop-oldest / drop-newest + metrics!), **prefetch limits** (RabbitMQ `prefetch=10`, Kafka `max.poll.records`), **consumer lag alerts** (10k stuck >5min = page!), **shed** (503 + Retry-After upstream — topic 02!). Demo all three policies in `../examples/04_semantics_dlq.py`.

One-liner: **"Compete → queue, broadcast → pub/sub, replay → log; SNS fans out to SQS queues; bound every buffer and alert on lag."**
