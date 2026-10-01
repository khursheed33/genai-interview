# 06 — GenAI Designs II: Platforms, Gateways & Voice (multi-tenant/agent/gateway/pipes)

## 1. Multi-tenant LLM platform (one kitchen, 100 restaurants!)

- Isolation: **silo** (dedicated stack per big tenant — $$$, compliance!) vs **pool** (shared + `tenant_id` EVERYWHERE — cheap, leak-risk!) vs **bridge** (shared compute, separate data planes!). Pool + row-filters + per-tenant keys/quotas/budgets is the default answer.
- Control plane: onboarding (provision namespace + keys + quotas!), metering (tokens/request/latency per tenant → bills!), rate pies (noisy-neighbor bulkheads!), evals per tenant (drift alerts!).

## 2. AI agent platform (workers with tools + brakes!)

Sandboxed tool runtime (least-privilege creds per run!) + approval gates (pay/refund = human click!) + trajectory logs (every thought+tool+result — topics 20/21!) + budgets (max $/steps/time per task!) + kill-switch. Multi-agent: supervisor + specialists + shared blackboard (topic 20 patterns!). State in DB (checkpoint/resume!), queues between agents (topic 08!).

## 3. LLM gateway (one door, many brains! — runnable `../examples/08_llm_gateway.js`)

```
auth/quota -> PII scrub -> semantic cache? -> ROUTE (quality/cost/latency rules!) -> provider
-> fallback (retry next!) -> log usage (tokens/$/latency per tenant!) -> stream back (SSE!)
```

- Routing: haiku-class for easy (classifier!), frontier for hard; contest: cheapest-first with quality floor. Fallbacks: same-tier next provider (outage-proof!). Budgets: per-key daily caps + alerts at 80% (topic 23 billing!).

## 4. Pipes: voice, doc-pipeline, recs (same blocks, new toys!)

- **Voice**: mic → VAD → STT stream → LLM (stream!) → TTS stream → speaker (WebRTC!); budgets: <800ms turn-taking (barge-in!), history summarizer (context cap!).
- **Doc pipeline** (OCR+LLM): upload → OCR/layout → classify → extract (schema!) → human-review queue (low-confidence!) → index. Idempotent stages + DLQ per stage (topic 08!).
- **Embedding recs**: nightly batch embeddings → ANN index → realtime rerank (rules+freshness!) → explore/exploit (bandits!) → feedback loop (clicks retrain!).

One-liner: **"Pool with tenant-filters + budgets, agents sandboxed + gated + logged, gateway routes+caches+falls-back, pipes stream under 800ms."**
