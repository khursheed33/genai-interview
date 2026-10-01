# 09 - System Design

> Scope: README.md section 9: scalability/latency/SLOs, estimation, hashing/bloom/rate-limiters, distributed transactions/consensus, classic designs + GenAI designs (RAG at scale, agent platform, LLM gateway), HLD/LLD/ADRs
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- Scale → `notes/01-scale-slo-estimation.md` (vertical/horizontal, latency/SLO/nines, napkin math)
- Glue → `notes/02-blocks-glue.md` (kit blocks, sharding, idempotency/2PC, Raft/Paxos/gossip, RPO/RTO)
- Classics I → `notes/03-classics-1.md` (shortener, limiter, notify + formula!)
- Classics II → `notes/04-classics-2.md` (chat/feed, video/files, crawler/autocomplete)
- GenAI I → `notes/05-genai-rag.md` (RAG at scale, enterprise Q&A, search/code-assistant)
- GenAI II → `notes/06-genai-platforms.md` (multi-tenant, agents, gateway, voice/pipes)
- Docs → `notes/07-docs-adr.md` + `notes/adr-001-*.md`, `adr-002-*.md` (HLD/LLD/C4 + 2 real ADRs!)

## Examples (8 runnable — verified)
| File | Covers | Run |
|---|---|---|
| `examples/01_estimation.py` | napkin toolkit + nines | `uv run python topics/09-system-design/examples/01_estimation.py` |
| `examples/02_bloom.py` | 12KB filter, ~1% FP | same pattern |
| `examples/03_url_shortener.py` | base62 + TestClient mini-service | same pattern |
| `examples/04_limiter_distributed.py` | central + local + cells | same pattern |
| `examples/05_raft_election.py` | split 2-2 → leader | same pattern |
| `examples/06_fanout_cost.py` | push/pull threshold math | same pattern |
| `examples/07_rag_scale.py` | 61GB + $6→$3 per 1k | same pattern |
| `examples/08_llm_gateway.js` | route/cache/fallback/bill | `node .../08_llm_gateway.js` |

## Exercises (5 — `uv run pytest topics/09-system-design/exercises -q`, 9 tests)
- `exercise-01-napkin` — Linkly QPS/storage/BW/boxes
- `exercise-02-bloom-size` — formulas + behavior
- `exercise-03-shortcode` — roundtrip + allocator
- `exercise-04-quorum-vote` — overlap + Raft round
- `exercise-05-rag-budget` — GB + $/mo + fleet

## Structure
- `README.md` - this checklist entry point
- `notes/` - your condensed notes (add `.md` per sub-topic)
- `examples/` - runnable minimal examples (python/js/sh)
- `exercises/` - practice tasks + solutions
- `interview-questions.md` - Q and A bank

## How to use
1. Read the checklist item in root README.
2. Add notes + code + diagrams here.
3. Do 2-3 exercises and 1 mini-project link in `projects/` if applicable.
4. Self-quiz with interview questions.

## Resources
- Add links as you learn (docs, papers, videos).
- Prefer primary sources: official docs, RFCs, papers.

## Progress
- [x] Notes drafted (7 + 2 ADRs, formula-first stories)
- [x] Examples run (8 files, verified: estimators + sims + node gateway)
- [x] Exercises done (5 exercises, 9 pytest tests green)
- [x] Interview Qs revised (20+ Q/A in `interview-questions.md`)
