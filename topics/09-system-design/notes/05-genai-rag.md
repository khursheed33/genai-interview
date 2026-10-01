# 05 — GenAI Designs I: RAG at Scale (chatbot/doc-Q&A/semantic/code-assistant)

The GenAI formula (classic formula + 3!): **requirements → estimation (tokens+$!) → data plane (ingest/chunk/index!) → serving plane (retrieve→rerank→generate!) → evals+guardrails (topics 21/24!) → cost/latency levers**. Always ask: freshness? tenants? citations? budget per 1k queries?

## 1. RAG chatbot at scale (the flagship!)

```
ingest: connectors -> parse/OCR -> clean/PII-scrub -> chunk (512t + overlap!) -> embed (batch!)
  -> vector DB (HNSW!) + metadata + ACL tags!
serve: query -> guard (injection!) -> rewrite/HyDE -> hybrid retrieve (dense+sparse!) -> rerank (top 50->5!)
  -> assemble (citations!) -> LLM stream (SSE!) -> eval-log (faithfulness!)
```

- Numbers (planner in `../examples/07_rag_scale.py`!): 1M docs × 20 chunks × 768d × 4B ≈ 60GB vectors (+metadata!). 100 QPS × (50ms embed + 100ms search + 2s LLM) — LLM DOMINATES (GPUs = budget!). Cache: exact (30% hits!) + semantic (20% more!) = half the GPUs (topic 07!).
- Freshness: CDC → re-chunk → versioned re-index (blue/green indexes, alias flip!). Deletes: tombstone + purge (GDPR!). Multi-tenant: namespace/filter + per-tenant keys (leak = career-ending!).

## 2. Enterprise doc Q&A (RAG + suits!)

Add: connectors (SharePoint/Drive/Slack!), **document-level ACLs** (retrieve THEN filter by `allowed_groups` — never leak via similarity!), audit (who saw doc 7!), PII redaction BEFORE index, evals per department (golden sets!), on-prem/VPC option (topic 24!). Answers carry citations + "I don't know" (abstention beats hallucination!).

## 3. Semantic search & code assistant (siblings!)

- Search: query embed → ANN top-k → business-rules rerank (freshness/authority!) → highlight. Hybrid (BM25 + dense RRF!) beats either alone. Click logs → eval (NDCG!).
- Code assistant: repo index (chunk by SYMBOL not lines! + dependency edges!), context budget (20k of 128k for retrieval, rest for reasoning!), completion cache (exact prefix hits 40%!), sandboxed execution (topic 25!), telemetry (accept-rate!).

One-liner: **"Ingest versioned + ACL-tagged, serve retrieve→rerank→stream, eval everything, cache halves GPUs, tenants never share keys."**
