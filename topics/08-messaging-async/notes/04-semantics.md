# 04 — Semantics: Promises, Poison & Floods (delivery + DLQ + ordering)

## 1. The three promises (say with the matrix!)

| Promise | How | Cost | Use |
|---|---|---|---|
| **At-most-once** (0/1) | commit/ack BEFORE work; no retry | may LOSE | metrics, heartbeats (losable!) |
| **At-least-once** (1+) | ack AFTER work + retry | DUPLICATES (the norm!) | everything important (pair with idempotency!) |
| **Effectively-once** | at-least + **idempotent consumer** | design effort | money, inventory, LLM charges (keys! dedupe table!) |

- Idempotency: `processed_ids` set / DB unique key on `event_id` / `UPDATE … WHERE version` — check-then-act ATOMICALLY (race double-process otherwise!).
- Kafka EOS / SQS FIFO dedupe (`MessageDeduplicationId` 5-min window!) help INSIDE the pipe; edges still need YOUR keys.

## 2. Poison & DLQ (don't let one rotten mango stop the truck!)

Retry 3–5× (backoff+jitter — topic 02!) → park in **DLQ** + alert (with headers: tries, first-error, trace!). Main queue flows; team inspects/replays DLQ (replay = resend with SAME id — idempotency saves you twice!). SQS: `maxReceiveCount + redrive`; RabbitMQ: DLX; Kafka: DLQ topic (+ headers!).

## 3. Ordering (per-key promises!)

- Kafka: same key → same partition (order!). SQS FIFO: `MessageGroupId` (per-group order + dedupe!). Service Bus: **sessions**. Global order = single partition/group (throughput sacrifice — shard by tenant to keep both!).
- Retries break order (1 fails, 2 succeeds → 2-before-1!). Strict order needs: stop-and-wait per key (slow!) or versioned apply (`apply only if seq = last+1, else park!`).

Runnable (all 3 semantics + DLQ + backpressure policies): `../examples/04_semantics_dlq.py`.
