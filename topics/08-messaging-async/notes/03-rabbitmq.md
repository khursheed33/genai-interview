# 03 — RabbitMQ: Smart Postmen (exchanges, routing, acks)

Kafka is a diary; RabbitMQ is a **sorting office** — the EXCHANGE routes, queues hold, consumers ack.

## 1. Exchanges (4 postmen — topic/fanout/direct/headers!)

| Type | Routes when | Use |
|---|---|---|
| **direct** | exact key match (`pay` → Q-pay) | task types |
| **fanout** | EVERYONE bound (ignores key!) | SNS-style broadcast (order-paid → 3 queues!) |
| **topic** | pattern `*.blr.*`, `#` = many words | `order.placed.blr` → blr-queue AND audit-queue (`order.#`)! |
| **headers** | header match (rare, slow) | multi-attr routing (skip unless asked!) |

Binding = "queue Q wants exchange E's mail matching pattern P". Dead-letter exchange (`x-dead-letter-exchange`) per queue = poison routing (retries → DLQ — note 04!).

## 2. Delivery promises (ack = "got it, mine now!")

- **Manual ack AFTER work** (auto-ack loses on crash!). `nack(requeue=True)` = retry later; `reject` = dead-letter. **Prefetch** (`basic.qos(prefetch=10)`) = max unacked per consumer (fair share + backpressure — without it, fast starter hogs all!).
- **Durability**: durable exchange + durable queue + persistent delivery (`delivery_mode=2`) — ANY missing piece = lost on restart. **Quorum queues** (Raft-replicated, modern default!) over classic mirrors.
- **Delayed**: no native delay — TTL + DLX bounce pattern (or delayed-message plugin); idempotent handlers make redelivery safe!

Runnable sorting office (all 3 exchanges + ack/requeue + prefetch): `../examples/03_rabbitmq_sim.py`.
