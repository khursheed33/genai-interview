# 07 — Design Docs: Blueprints & Decision Diaries (HLD/LLD/C4/ADR)

## 1. HLD vs LLD (city map vs wiring diagram!)

- **HLD**: boxes + arrows (gateway→API→cache→DB→queue), data flow, scale numbers, failure plan. Audience: everyone. Fits one page!
- **LLD**: schemas, APIs (OpenAPI!), state machines, sequence diagrams (login→token→refresh!), class/ER diagrams, error tables. Audience: builders. Lives with code!
- **C4**: Context (users+systems!) → Container (apps/DBs!) → Component (modules!) → Code (zoom as needed!). UML when precise (sequence/class/ER), C4 when aligning (stakeholders!).

## 2. ADR (decision diary — the promotion file!)

Every big choice gets a numbered record: context → options → decision → consequences (good + BAD + mitigations!). Template + 2 real ones live here:

- `adr-001-vectors-in-postgres.md` (pgvector now, dedicated later — when!)
- `adr-002-sse-for-tokens.md` (SSE over WS for one-way streams!)

Write BEFORE building (forces trade-off thinking!), review like code, SUPERSEDE (never edit history — ADR-009 supersedes ADR-002!). Interviews: "tell me a hard decision" = read your newest ADR aloud!

One-liner: **"HLD one page for all, LLD with code for builders, C4 to align, ADRs to remember WHY (supersede, never rewrite)."**
