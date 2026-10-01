# Interview Scenario Notes

## Reusable framework
Clarify requirements → quantify scale → identify bottleneck → propose the smallest useful change → handle failure/security → define measurement → explain trade-offs.

## Slow RAG and hallucinations
Measure ingestion, retrieval, reranking, model TTFT, generation, and network separately. Determine whether hallucination comes from missing knowledge, bad retrieval, stale data, or unsupported generation. Add grounding and verification where appropriate.

## Scale and cost
For 100 → 1M users, revisit database capacity, caches, queues, rate limits, autoscaling, observability, and failure isolation. Do not multiply every component blindly.

## Security and tenancy
Use least privilege, tenant-aware authorization, secret isolation, audit logs, and independent tool checks. A prompt is not an authorization mechanism.

## Reliability
For outages, mitigate first, then identify root and contributing causes. For zero-downtime migrations use backward-compatible schemas, staged rollout, health checks, and rollback plans.

## Practice scenarios
Design multi-tenant RAG, migrate a monolith, secure an agent, index very large documents, choose workflow vs agent, build an evaluation system, recover from an incident, and debug proxy/SSL/DNS failures.

## Interview habit
State assumptions explicitly and explain what you would measure next. Strong answers show how you would discover that your hypothesis is wrong.