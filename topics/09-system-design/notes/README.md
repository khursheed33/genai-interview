# System Design Notes

## Mental model
Start with requirements, scale estimates, APIs, data, then architecture. Separate functional requirements from latency, availability, consistency, durability, security, and cost constraints.

## Core building blocks
Load balancers distribute traffic. Caches reduce repeated work but require TTL/invalidation decisions. Queues absorb bursts and decouple producers from consumers but introduce retries, duplicates, ordering, and DLQs. Replication improves availability/read capacity but can lag. Sharding scales data but complicates joins, transactions, hot keys, and rebalancing.

## Distributed techniques
Consistent hashing limits data movement when nodes change. Bloom filters provide compact probabilistic membership checks. Token buckets and sliding windows enforce rate limits. Use outbox/saga patterns when a workflow spans independent services. Consensus is for distributed agreement, not ordinary CRUD transactions.

## GenAI systems
For an LLM gateway or RAG system model client → gateway → policy/rate limit → cache/model → retrieval/tools → response. Measure token usage, model latency, retrieval latency, context size, failures, and cost.

## Practice
Estimate a 1M-user service, design a URL shortener, notification service, large-scale RAG, and LLM gateway. For every design explain one bottleneck and one trade-off.