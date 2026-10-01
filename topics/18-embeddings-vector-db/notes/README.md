# Embeddings and Vector Databases Notes

## Embeddings
An embedding maps an object such as text into a numeric vector so semantic relationships can be compared geometrically. Dense embeddings capture meaning; sparse representations such as BM25 emphasize lexical matches.

## Similarity
Cosine similarity compares vector direction. Dot product depends on both direction and magnitude. Euclidean distance measures geometric separation. The correct metric depends on the embedding model and index configuration.

## ANN search
Exact nearest-neighbor search becomes expensive at scale. Approximate methods such as HNSW and IVF trade some recall for speed and memory efficiency. HNSW builds a navigable graph; IVF partitions the vector space into candidate regions.

## Hybrid retrieval
Dense search can miss exact identifiers; lexical search can miss paraphrases. Hybrid retrieval combines both. Reciprocal Rank Fusion is a simple way to combine rankings without requiring scores to be directly comparable.

## Filtering and tenancy
Metadata filters should be applied in a way that preserves tenant isolation. A user must never receive another tenant's vector or document simply because it is semantically similar.

## Practice
Compare cosine and dot product, build a small exact search, simulate ANN recall, combine BM25 with dense results, and design tenant-safe metadata filtering.