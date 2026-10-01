# Data Engineering for GenAI Notes

## Data lifecycle
A GenAI data pipeline typically performs ingestion → parsing → normalization → quality checks → deduplication → PII handling → enrichment → chunking/embedding → indexing → monitoring.

## ETL and ELT
ETL transforms before loading; ELT loads raw data and transforms within the analytical platform. Airflow coordinates workflows; dbt focuses on SQL-based transformation, testing, and lineage.

## Storage and processing
Columnar formats such as Parquet are efficient for analytical scans. Pandas is convenient for many in-memory workloads; Polars emphasizes fast columnar execution. Object storage is commonly used for durable data lakes.

## Incremental indexing
Do not reprocess everything when only a small portion changed. Use CDC, timestamps, content hashes, document versions, and tombstones. Make indexing jobs idempotent so retries do not create duplicate records.

## Quality and governance
Measure schema validity, completeness, duplication, freshness, source provenance, permission state, and PII exposure. Version data and transformations so an answer can be traced to the source material used.

## Search basics
TF-IDF weights terms by frequency and inverse document frequency. BM25 improves practical lexical retrieval through term-frequency saturation and document-length normalization.

## Practice
Build an incremental document pipeline, add deduplication and PII checks, store Parquet, index changed documents only, and evaluate BM25 against a small query set.