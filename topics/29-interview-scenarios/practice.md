# Practice Guide

## Scenarios
1. RAG is too slow.
2. Answers hallucinate despite retrieval.
3. Model cost doubled at scale.
4. A dependency rate-limits the service.
5. An LLM tool call performs an unsafe action.
6. A tenant can see another tenant's documents.
7. A monolith needs gradual migration.
8. A zero-downtime schema change is required.
9. Large documents exceed context limits.
10. An agent loops and consumes budget.
11. An evaluation score regresses after a model change.
12. Production fails due to proxy/SSL/DNS configuration.

## Answer format
State assumptions → quantify → isolate the failure → propose changes → discuss trade-offs → define measurements → explain rollback or follow-up.

## Deliverable
Record a 5–10 minute spoken answer for each scenario and then write the architecture or diagnostic steps in Markdown.