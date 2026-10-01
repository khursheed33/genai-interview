# Exercise 05 — Price the Chatbot (RAG budget + cache levers)

**Story:** Finance asks "what does 50k queries/day cost?" Show math + cache savings.

## Task
In `solution.py`:
- `vector_gb(docs, chunks, dim, bytes_=4)` → GB float
- `monthly_cost(queries_per_day, tokens_per_q, usd_per_m, cache_hit=0.0)` → billed queries pay full; cache hits FREE
- `gpus_needed(qps, sec_per_query, per_gpu=1)` → ceil(qps × sec / per_gpu)

## Acceptance
- 1M docs × 20 × 768 × 4B ≈ 61GB; 50k/day × 3k tokens × $2/M ≈ $9k/mo pre-cache; 50% hits halves it; 100 QPS × 2s → 200 streams
