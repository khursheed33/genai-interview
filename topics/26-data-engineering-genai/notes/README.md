# Data Engineering for GenAI Notes

## Lifecycle
A GenAI data pipeline often performs ingestion → parsing → normalization → quality checks → deduplication → PII handling → enrichment → chunking/embedding → indexing → monitoring.

## ETL and ELT
ETL transforms before loading; ELT loads raw data and transforms inside the data platform. Airflow coordinates workflows; dbt focuses on SQL transformation, tests, and lineage.

## Storage
Parquet is a columnar format suited to analytical scans. Pandas is convenient for in-memory work; Polars emphasizes fast columnar execution. Object storage is commonly used for durable data lakes.

## Incremental indexing
Use CDC, timestamps, content hashes, document versions, and tombstones to process changes without rebuilding everything. Make indexing idempotent so retries do not duplicate records.

## Search
TF-IDF weights terms by frequency and inverse document frequency. BM25 improves practical lexical retrieval through term-frequency saturation and document-length normalization.

## Practice
Build an incremental document pipeline, add deduplication and PII checks, store Parquet, index changed documents only, and evaluate BM25 on a small query set.