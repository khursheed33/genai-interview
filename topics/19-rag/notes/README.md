# RAG Notes

## What RAG solves
RAG retrieves external information at query time and gives that context to a generator. It is useful when knowledge changes frequently, must be sourced, or is too large to encode reliably in model parameters. Fine-tuning is more appropriate for behavior/style/task adaptation than rapidly changing facts.

## Pipeline
Ingestion → parsing → cleaning → chunking → metadata → embedding/indexing → query rewriting → retrieval → reranking → context assembly → generation → citations/evaluation.

## Chunking and retrieval
Chunks should preserve meaningful context. Structure-aware chunking can preserve headings, tables, and sections. Store document ID, tenant, source, timestamp, permissions, and version. Dense retrieval captures semantics; sparse retrieval captures exact terms; hybrid retrieval combines them. Reranking improves candidate ordering and MMR can reduce redundancy.

## Advanced patterns
Corrective/self-reflective RAG can retry weak retrieval. Agentic RAG lets an orchestrator choose retrieval/tool actions. GraphRAG represents relationships explicitly. Conversational RAG must distinguish conversation context from authoritative evidence.

## Failure modes
Diagnose bad parsing, poor chunks, missing filters, low recall, irrelevant context, stale documents, permission leaks, and unsupported answers separately.

## Practice
Build a tiny RAG pipeline, compare chunk sizes, test dense vs hybrid retrieval, add reranking and tenant filtering, and create an evaluation set containing answerable and unanswerable questions.