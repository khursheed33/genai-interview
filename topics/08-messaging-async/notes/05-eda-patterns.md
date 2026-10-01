# 05 — EDA Patterns: Diary, Two Desks & Relay Races (sourcing/CQRS/saga/outbox)

## 1. Event-driven architecture (react, don't call!)

Services emit facts (`OrderPaid`) and move on; others subscribe (warehouse, email, fraud — independent deploy/scale!). Cost: eventual consistency + observability (trace-id through EVERY hop — topic 14!) + schema discipline (registry + compat: ADD optional only!).

## 2. Event sourcing (diary IS the truth!)

Store EVENTS (`Credited 50`, `Debited 30`), derive state by **fold** (`balance = Σ`). Superpowers: audit free, **time-travel** (balance last Tuesday!), rebuild by replay, debug by re-running. Costs: snapshots (fold 1M events each read? cache every 1000th!), versioning (V1/V2 events + upcasters!), GDPR erasure vs immutable log (crypto-shredding: encrypt per-user, delete KEY!). Demo fold + snapshot + time-travel: `../examples/07_sourcing_cqrs.py`.

## 3. CQRS (two desks: writes desk + read desks!)

Commands → write model (normalized, strict) → events → **projections** build read models (denormalized per view: search index, dashboard, feed!). Scale/read-shape independently; accept lag (UI: "updating…" + version stamps!). Same split as topic 06's read models.

## 4. Saga (relay race with undo legs!)

No distributed TX across services → chain LOCAL txs + **compensations** (refund the payment, restock the shelf!):

- **Choreography** (dancers listen): `OrderCreated → Pay → Paid → Stock → Shipped`; failure event triggers compensations back. Simple start, spaghetti at 10 services (who watches the dance?!).
- **Orchestration** (conductor!): saga service commands each step, runs compensations REVERSED on failure. Visible + testable — pick beyond 3 steps!
- Compensations must be IDEMPOTENT + retryable (refund twice = bug!). Demo both: `../examples/05_saga_outbox.py`.

## 5. Outbox (the atomic lie-detector!)

Dual-write (DB + publish) fails halfway → ghost rows OR ghost events. Fix: **write event to OUTBOX table in the SAME DB transaction**, relay publishes (CDC/Debezium tails the log — no polling!), consumer dedupes by `event_id`. Inbox table on the receiving side completes the exactly-once illusion. Demo relay + dedupe in `../examples/05_saga_outbox.py`.

One-liner: **"Diary for truth, two desks for scale, sagas with undo legs, outbox kills dual-write ghosts."**
