# 05 — NoSQL Atlas: Five Countries (doc/kv/wide/graph/search + time)

Pick by ACCESS pattern, not hype. Same data, five passports:

## 1. The five (+ flagship + partition thinking)

| Type | Story | Flagship | Partition/shard key thinking |
|---|---|---|---|
| Document | folder per order (JSON inside) | **MongoDB** | shard by `customer_id` (all one's orders together!) |
| Key-Value | locker wall (opaque blobs) | Redis/DynamoDB | key IS the address (hash it!) |
| Wide-column | spreadsheet with 1M columns per row | **Cassandra/DynamoDB** | partition key (which node) + clustering key (order ON node!) |
| Graph | family tree with labeled arrows | **Neo4j** | traversals, not shards (see note 06!) |
| Search | book index building | **Elasticsearch/OpenSearch** | shards by routing; replicas for read fan-out |
| (+Time-series: append-only meter readings — Influx/Timescale/ClickHouse; note 07) |

## 2. MongoDB (embed vs reference + pipeline)

```js
// EMBED (one fetch!): order with items inside — reads together, writes together
{ _id: 7, items: [{name: "dosa", qty: 2}], status: "paid" }
// REFERENCE (many-to-many / unbounded!): reviews live apart, order holds ids
{ _id: 7, review_ids: [ObjectId("..."), ...] }   // 16 MB doc cap says: comments out!
```

- Rule: **embed when read-together + bounded; reference when shared/unbounded/grown** (user↔orders, post↔10k comments).
- **Aggregation pipeline** = conveyor: `$match → $group → $sort → $project` (mini-engine in `../examples/05_doc_pipeline.py`). Indexes per query shape; **replica sets** (1 primary + voters, auto-failover) for HA; **sharding** (`customer_id` hashed) for scale + zone pinning.

## 3. Cassandra/DynamoDB (write-first world)

- Model QUERIES first: `PRIMARY KEY ((tenant, day), event_ts)` — partition spreads load, clustering sorts retrieval. **Hot partition** (celebrity tenant!) = throttles → salt/split keys.
- **Consistency dial**: `ONE / QUORUM / ALL` (reads+Writes tune: `R+W > N` = strong-ish, see note 07!). Dynamo **GSI/LSI**: alternate doors into same data (by-status, by-date indexes with own throughput!).

## 4. Elasticsearch (inverted index + BM25 + analyzers)

`dosa` → `[doc7, doc19…]` (term→docs!). **Analyzer** chain: lowercase → tokenize → stopwords → stem (`running→run`) — same analyzer at index AND query time (mismatch = zero hits, classic!). **BM25** = TF (frequent here?) × IDF (rare everywhere?) × length-norm (short docs win ties) — from-scratch demo in `../examples/06_bm25_search.py`. Mappings: `text` (search) vs `keyword` (sort/aggregate/exact!) — wrong choice = broken dashboards.
