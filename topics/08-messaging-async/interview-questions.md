# Interview Questions — Messaging & Async Processing

Say the **bold line** first, then the hook.

## Patterns & Kafka

- [ ] **[theory]** Queue vs pub/sub vs log — one promise each + managed pick?
  - **Queue = one consumer (SQS). Pub/sub = all hear (SNS). Log = replayable offsets (Kafka). SNS fans out to SQS = best of both.**
- [ ] **[hands-on]** Same key same partition how? 12 partitions, 4 consumers — deal?
  - **Hash key % N; group deals round-robin (3 each); death → rebalance (cooperative softens).**
- [ ] **[theory]** Offsets: commit when? Lag = ? Retention vs compaction?
  - **After work (at-least!) or before (at-most, may skip). Lag = end−committed (THE metric). Delete by age/size; compact keeps last-per-key (changelog!).**
- [ ] **[theory]** Kafka exactly-once, honestly? Unclean leader?
  - **Idempotent producer + transactions inside Kafka; effectively-once at edges via YOUR idempotency keys. Unclean election NEVER (loss for uptime — refuse!).**

## RabbitMQ & semantics

- [ ] **[hands-on]** Direct vs fanout vs topic + `order.*.blr` vs `order.#`?
  - **Exact / all / patterns (`*`=one word, `#`=rest). Manual ack AFTER work; prefetch = fair share + backpressure; durable everything + quorum queues.**
- [ ] **[theory]** At-most vs at-least vs effectively-once + FIFO dedupe?
  - **Ack-before (may lose) / ack-after+retry (dupes — the norm!) / +idempotent consumer (money!). SQS FIFO dedupe = 5-min window only.**
- [ ] **[hands-on]** Poison handling end-to-end? Ordering with retries?
  - **3–5× backoff → DLQ + headers + alert; replay same ids. Order per key/partition/group; retries break strict order (stop-and-wait or seq-park to fix).**
- [ ] **[theory]** Backpressure three policies + lag alert?
  - **Block / drop-oldest / drop-newest — bounded always! Alert lag depth+age (10k >5min = page).**

## EDA, processing, orchestration

- [ ] **[theory]** Event sourcing superpowers + costs? CQRS split?
  - **Fold for truth, time-travel, replay rebuilds; costs snapshots + versioning + GDPR crypto-shredding. CQRS: write desk + projected read desks (accept lag!).**
- [ ] **[hands-on]** Choreography vs orchestration saga + compensation rules?
  - **Dancers-listen (2 steps) vs conductor (3+). Compensate REVERSED, idempotent + retryable. Outbox (same-TX event + relay + dedupe) kills dual-write ghosts.**
- [ ] **[theory]** Batch vs stream vs Kappa? Windows + watermarks?
  - **Nightly census vs live ticker; Kappa = one log reprocessed. Tumbling/sliding/session windows on EVENT-time; watermarks park stragglers.**
- [ ] **[theory]** Airflow vs Temporal vs Step Functions + 3 rules?
  - **DAGs+backfill / durable code-resume / visual states. Tasks idempotent, workflows versioned, humans as steps (+timeouts/heartbeats!).**

## Gotchas (say unprompted)

- Auto-ack loses on crash; commit-before-work skips; global order = throughput sacrifice.
- Dual-write without outbox = ghosts; non-idempotent compensation refunds twice.
- `now()` inside stream transforms breaks replays; unbounded buffers OOM.

## Self-score (0–5)

- Patterns+Kafka: __ / Rabbit+semantics: __ / EDA+saga: __ / processing+orch: __
- Whiteboard: partition deal + topic match + saga undo + outbox? Y/N each.
