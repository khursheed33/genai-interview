# Interview Questions — System Design

Design rounds test THINKING, not memory. Open every answer with the formula, then numbers.

## Formula & fundamentals

- [ ] **[theory]** The 6-step formula + what you clarify first?
  - **Requirements → estimation → API → HLD → deep dive (1–2!) → bottlenecks/trade-offs. Clarify: scale, read:write, consistency, latency, budget — numbers drive every choice.**
- [ ] **[hands-on]** Size it: 5M DAU × 3 writes, 8:1 reads, 500B rows?
  - **~868 writes/s peak, ~7k reads, ~675GB/mo (×3!), ~5 boxes + headroom. (Toolkit: `examples/01`, exercise-01.)**
- [ ] **[theory]** p99 vs avg? SLI/SLO/SLA + error budget? Nines for 99.9?
  - **Avg lies, tails kill (p99!). SLI measured → SLO promised → SLA contracted. Budget = 1−SLO (43min/mo at 99.9; 8.7h/yr). Burnt budget = freeze features.**
- [ ] **[theory]** Vertical vs horizontal? Stateless scaling needs?
  - **Bigger box (ceiling!) vs more boxes (needs stateless + LB + shared state). Sticky/stateful = last resort.**

## Blocks & classics

- [ ] **[hands-on]** Shortener: counter vs hash? 301 vs 302? 100M/mo storage?
  - **Counter+base62 (ordered, no collisions; range allocator!). 301 permanent (cached) vs 302 (count clicks). ~150GB/mo with replicas.**
- [ ] **[theory]** Rate limit at scale: local vs central? Headers?
  - **Central Redis exact + local fast-path + sticky cells. `Remaining + Retry-After` on 429; per-endpoint costs (LLM = token budget!).**
- [ ] **[hands-on]** Chat/feed: push vs pull + celebrity math?
  - **Push normals (fast reads), pull stars (10M writes melt!). Threshold ~10k; cursor pages; presence via heartbeat+TTL.**
- [ ] **[theory]** Video pipeline in 4 hops? Crawler politeness + dedupe?
  - **Presigned upload → transcode ladder → HLS chunks on CDN → signed URLs. Crawl: priority frontier + 1 req/s/host + robots + SimHash/bloom dedupe.**
- [ ] **[hands-on]** Bloom sizing 1M URLs at 1%? No false...?
  - **~9.6M bits + 7 hashes (double-hashing!). NEVER false negatives; ~1% FP (pair with cached-NULLs!).**
- [ ] **[theory]** Raft in 60s: majority, split, terms?
  - **Majority wins (>n/2); even clusters split 2-2 → jittered retry; higher term steps down stale bosses; heartbeats hold leases.**

## GenAI designs & docs

- [ ] **[scenario]** RAG at scale: storage + QPS + cost for 1M docs, 100 QPS?
  - **~61GB vectors + metadata; embed+search ≪ 2s LLM (GPUs = budget!); exact+semantic cache halves fleet; versioned re-index + tenant filters + citations + eval logs.**
- [ ] **[scenario]** Enterprise doc Q&A extras over basic RAG?
  - **Connectors, document ACLs at retrieval, audit trail, PII-scrubbed index, per-dept golden evals, abstention + VPC option.**
- [ ] **[scenario]** LLM gateway must-haves? Multi-tenant isolation flavors?
  - **Auth/quota → scrub → cache → route (difficulty/cost) → fallback → per-tenant billing. Silo ($$$) vs pool+filters (default!) vs bridge.**
- [ ] **[scenario]** Agent platform brakes? Voice budget?
  - **Sandboxed tools + approval gates + trajectories + $/step budgets + kill-switch. Voice: <800ms turns (stream STT→LLM→TTS, barge-in, summary memory!).**
- [ ] **[theory]** HLD vs LLD vs C4? ADR anatomy + when to write?
  - **HLD one-pager for all; LLD schemas+sequences with code; C4 zoom levels. ADR: context→options→decision→consequences; BEFORE building; supersede never rewrite.**

## Gotchas (say unprompted)

- No clarification = wrong design; avg without peak = outage; global order = throughput sacrifice.
- Unbounded context/cost in GenAI (budgets + caches FIRST!); tenants sharing keys = leak.
- Missing citations/evals = hallucination liability; no alias-flip re-index = serving mixed versions.

## Self-score (0–5)

- Formula+estimation: __ / classics: __ / distributed glue: __ / GenAI designs: __ / docs: __
- Whiteboard: shortener HLD + fan-out math + RAG capacity + one ADR? Y/N each.
