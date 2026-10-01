# 06 — Processing: Census vs Live Ticker (batch vs stream, windows, Spark/Flink)

## 1. Batch vs stream (census office vs stock ticker!)

| | Batch (Spark) | Stream (Flink/Kafka Streams) |
|---|---|---|
| Reads | bounded files/tables (nightly!) | endless events (now!) |
| Latency | minutes–hours | ms–seconds |
| Replays | re-run job (deterministic!) | rewind offsets (same!) |
| Use | billing, ML training, warehouse marts | fraud block, live leaderboard, LLM guardrails! |

- **Lambda** (batch + speed layers, merge pain!) vs **Kappa** (ONE stream log, reprocess for history — modern default!). Micro-batch (Spark Structured Streaming: 100ms batches, simple!) vs true per-event (Flink: lower latency, harder!).

## 2. Windows (group the endless!)

**Tumbling** (fixed 5-min, no overlap: bills!), **sliding** (5-min every 1-min: smooth dashboards!), **session** (gap-based: user visits!), **global + trigger** (odd ones!). Late events: **watermarks** ("we've seen till 10:04, stragglers → side output!") + allowed lateness. Event-time (when happened — correct!) vs processing-time (when seen — easy, wrong during outages!).

## 3. Spark/Flink survival kit

- **Checkpointing + WAL** = exactly-once state (Flink barriers align snapshots; Spark writes idempotent sinks!). Backpressure built-in (credit-based!) — monitor it, don't fight it.
- Deterministic code (no `now()` inside transforms — pass event time!), keyed state (per-tenant isolation!), schema evolution (topic 05 discipline!), dead-letter side outputs (poison never kills the stream!).

One-liner: **"Kappa one log; windows group infinity (event-time + watermarks); checkpoint for EOS; late/poison to side outputs."**
