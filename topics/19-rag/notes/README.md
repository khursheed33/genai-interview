# RAG Notes

## What RAG solves
RAG retrieves external information at query time and gives that context to a generator. It is useful when knowledge changes frequently, must be sourced, or is too large to encode reliably in model parameters. Fine-tuning is more appropriate for behavior/style/task adaptation than for frequently changing facts.

## Pipeline
A production pipeline is ingestion → parsing → cleaning → chunking → metadata → embedding/indexing → query rewriting → retrieval → reranking → context assembly → generation → citations/evaluation.

## Chunking
Chunks should preserve meaningful context while remaining searchable. Fixed token windows are simple; structure-aware chunking can preserve headings, tables, and sections. Store metadata such as document ID, tenant, source, timestamp, permissions, and version.

## Retrieval
Dense retrieval captures semantic similarity. Sparse retrieval captures exact terms. Hybrid retrieval combines them. Reranking improves candidate ordering. MMR can reduce redundant results. HyDE generates a hypothetical answer/document to improve retrieval for some queries.

## Advanced patterns
Corrective/self-reflective RAG can detect weak retrieval and retry. Agentic RAG lets an orchestrator decide which retrieval/tool actions to take. GraphRAG represents relationships explicitly. Conversational RAG must separate conversation context from authoritative source evidence.

## Failure modes
Common failures are bad parsing, poor chunks, missing metadata filters, low recall, irrelevant context, stale documents, permission leaks, and unsupported answers. Diagnose retrieval and generation independently.

## Practice
Build a tiny RAG pipeline, compare chunk sizes, test dense vs hybrid retrieval, add reranking, add tenant filtering, and create an evaluation set containing answerable and unanswerable questions.