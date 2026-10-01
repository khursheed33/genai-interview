# ADR-002: SSE (not WebSockets) for LLM token streaming

- Status: accepted (2026-09-30) | Deciders: API team | Context: chat UX needs tokens-as-they-arrive

## Context

Tokens stream server→client (one direction!). Options: SSE, WebSockets, chunked JSON, polling.

## Options

1. **SSE** (`text/event-stream`, auto-reconnect, plain HTTP!)
2. WebSockets (bidi, stateful, LB sticky!)
3. Polling (simplest, laggiest)

## Decision

Option 1: SSE with `data:` frames + `[DONE]`, `Last-Event-ID` resume.

## Consequences

- Good: works through proxies/LB (plain HTTP!), auto-reconnect, no sticky needed, trivial client.
- Bad: one-way only (chat input stays POST — fine!), 6-conn browser cap (multiplex or HTTP/2!).
- Revisit if: collaborative editing/voice barge-in needs bidi (then WS — ADR-00Y!).
