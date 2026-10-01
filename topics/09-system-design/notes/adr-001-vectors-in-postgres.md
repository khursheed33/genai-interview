# ADR-001: Vectors in Postgres (pgvector) instead of a dedicated vector DB

- Status: accepted (2026-09-30) | Deciders: platform team | Context: RAG MVP, 2M chunks

## Context

Need ANN search for RAG now. Team knows Postgres; dedicated Qdrant/Milvus = new infra to learn + operate.

## Options

1. **pgvector in existing Postgres** (HNSW index, metadata filter in SQL!)
2. Dedicated Qdrant/Milvus cluster (faster at 100M+, hybrid built-in)
3. Elasticsearch kNN (already have ES for search!)

## Decision

Option 1: `pgvector` (`hnsw(m2m32, ef_construction 128)`), filters in SQL (`WHERE tenant_id`), metadata + vectors in ONE transaction (no dual-write ghosts!).

## Consequences

- Good: zero new infra, JOINs + ACL filters trivial, transactional consistency.
- Bad: single-node ceiling (~10–50M vectors), no built-in hybrid (add BM25 sidecar later!).
- Mitigations: shard key ready (`tenant_id`), re-index plan; revisit at 20M vectors or p99 >300ms (ADR-00X!).
