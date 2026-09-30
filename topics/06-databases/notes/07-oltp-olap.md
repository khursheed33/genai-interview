# 07 — OLTP vs OLAP: Shop Counter vs Census Office (row vs column, lake vs house)

## 1. The split (say this table!)

| | OLTP (shop counter) | OLAP (census office) |
|---|---|---|
| Questions | "order 7's status?" (one row, NOW) | "dosa trend by city × month?" (billions, history) |
| Shape | normalized rows, indexed lookups | denormalized stars, columnar scans |
| Engines | Postgres/MySQL (+read replicas) | **ClickHouse**, BigQuery, Snowflake, Redshift |
| Freshness | milliseconds | minutes–hours (ETL/ELT batches!) |

- **Columnar** (Parquet/ORC, ClickHouse): read 2 of 200 columns → skip 99% bytes (10–100× on analytics!). Compression loves same-type columns.
- **Time-series** (metrics/logs/IoT): append-only + retention (`DROP PARTITION` > `DELETE`), downsampling (1s→1min→1h rollups) — InfluxDB/TimescaleDB/ClickHouse.

## 2. Lake vs warehouse vs lakehouse (where do files sleep?)

- **Warehouse** (Snowflake/BigQuery): structured, governed, SQL-first, $$ per scan.
- **Lake** (S3 + Parquet): cheap, raw, any format — chaos without catalogs!
- **Lakehouse** (Delta/Iceberg/Hudi on S3): lake prices + warehouse tricks (ACID, time-travel, schema evolution). Pick per query wallet: hot dashboards → warehouse; cold ML training → lake.

Pipeline (topic 26 deep-dives): OLTP → CDC/Debezium → lake → dbt models → warehouse marts → BI. GenAI: embeddings + eval logs land in the LAKE (JSONL/Parquet), served from warehouse marts.

## 3. PG-flavored extras (bonus round)

- **JSONB**: flexible LLM metadata WITH GIN indexes (`WHERE meta->>'model' = 'gpt-4o'` indexed!) — schema-less where it wiggles, relational where it matters.
- **Full-text**: `to_tsvector/to_tsquery` + GIN (small search without ES!).
- **Partitioning**: declarative by range (monthly `orders_2026_01` — drop old months free!) + read replicas (async lag! don't read-your-write there) + failover (promote replica, repoint DNS — RPO/RTO in topic 09!).

One-liner: **"Counter = rows+replicas, census = columns+Parquet; lake cheap+raw, warehouse governed+fast, lakehouse both."**
