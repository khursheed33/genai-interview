# Progress Tracker

> Check off as you finish: notes + examples run + exercises + interview Qs.
> Status log lives below in [Completed log](#completed-log) — update it every time a topic is finished.

## Core Engineering
- [x] [01-programming-fundamentals](../topics/01-programming-fundamentals/) — done 2026-09-30 (see log)
- [x] [02-api-design-web-protocols](../topics/02-api-design-web-protocols/) — done 2026-09-30 (see log)
- [x] [03-backend-frameworks](../topics/03-backend-frameworks/) — done 2026-09-30 (see log)
- [x] [04-auth-security](../topics/04-auth-security/) — done 2026-09-30 (see log)
- [x] [05-networking-proxy-dns](../topics/05-networking-proxy-dns/) — done 2026-09-30 (see log)
- [x] [06-databases](../topics/06-databases/) — done 2026-09-30 (see log)
- [x] [07-caching](../topics/07-caching/) — done 2026-09-30 (see log)
- [x] [08-messaging-async](../topics/08-messaging-async/) — done 2026-09-30 (see log)
- [ ] [09-system-design](../topics/09-system-design/)
- [ ] [10-software-architecture](../topics/10-software-architecture/)
- [ ] [11-frontend-fullstack](../topics/11-frontend-fullstack/)
- [ ] [12-devops-cloud](../topics/12-devops-cloud/)
- [ ] [13-scripting-linux](../topics/13-scripting-linux/)
- [ ] [14-observability](../topics/14-observability/)
- [ ] [15-testing-quality](../topics/15-testing-quality/)

## GenAI
- [ ] [16-llm-fundamentals](../topics/16-llm-fundamentals/)
- [ ] [17-prompt-engineering](../topics/17-prompt-engineering/)
- [ ] [18-embeddings-vector-db](../topics/18-embeddings-vector-db/)
- [ ] [19-rag](../topics/19-rag/)
- [ ] [20-agents-orchestration](../topics/20-agents-orchestration/)
- [ ] [21-evaluation](../topics/21-evaluation/)
- [ ] [22-fine-tuning](../topics/22-fine-tuning/)
- [ ] [23-llm-serving-llmops](../topics/23-llm-serving-llmops/)
- [ ] [24-guardrails-safety](../topics/24-guardrails-safety/)
- [ ] [25-multimodal-genai](../topics/25-multimodal-genai/)
- [ ] [26-data-engineering-genai](../topics/26-data-engineering-genai/)
- [ ] [27-classical-ml-basics](../topics/27-classical-ml-basics/)

## Career
- [ ] [28-engineering-practices-soft-skills](../topics/28-engineering-practices-soft-skills/)
- [ ] [29-interview-scenarios](../topics/29-interview-scenarios/)

## Weekly log
| Week | Focus | Done | Interview-ready (0-5) |
| ---- | ----- | ---- | --------------------- |
| W1 (2026-09-30) | 01-programming-fundamentals | notes(8) + examples(13) + exercises(5/12 tests) + Q/A(25+) | 4 (pending self-quiz) |
| W1 (2026-09-30) | 02-api-design-web-protocols | notes(8) + examples(11) + exercises(5/12 tests) + Q/A(25+) | 4 (pending self-quiz) |
| W1 (2026-09-30) | 03-backend-frameworks | notes(7) + examples(7) + exercises(5/10 tests) + Q/A(20+) | 4 (pending self-quiz) |
| W1 (2026-09-30) | 04-auth-security | notes(8) + examples(8) + exercises(5/10 tests) + Q/A(20+) | 4 (pending self-quiz) |
| W1 (2026-09-30) | 05-networking-proxy-dns | notes(7) + examples(7) + exercises(5/10 tests) + Q/A(20+) | 4 (pending self-quiz) |
| W1 (2026-09-30) | 06-databases | notes(8) + examples(8) + exercises(5/7 tests) + Q/A(20+) | 4 (pending self-quiz) |
| W1 (2026-09-30) | 07-caching | notes(6) + examples(8) + exercises(5/9 tests) + Q/A(20+) | 4 (pending self-quiz) |
| W1 (2026-09-30) | 08-messaging-async | notes(7) + examples(8) + exercises(5/9 tests) + Q/A(20+) | 4 (pending self-quiz) |

## Completed log

### 2026-09-30 — 01-programming-fundamentals ✅
- **Notes (8):** `01-python-core`, `02-python-functions`, `03-python-oop-typing`, `04-python-async-tooling`, `05-javascript`, `06-typescript-node`, `07-dsa-big-o`, `08-solid-patterns-concurrency` — kid-style + real-world (Swiggy, tiffin, waiter).
- **Examples (13, all ran green):** `01_mutability.py`, `02_comprehensions_generators.py`, `03_decorators_context_managers.py`, `04_oop_dataclass_pydantic.py`, `05_async_demo.py` (2s→1s), `06_exceptions_logging.py`, `07_closures_this.js`, `08_promises_async.js`, `09_node_streams.js`, `10_dsa_patterns.py`, `11_patterns_solid.py`, `12_race_lock.py`, `13_typescript_demo.ts`.
- **Exercises (5, 12/12 pytest pass):** `exercise-01-mutable-default`, `exercise-02-generator`, `exercise-03-retry-decorator`, `exercise-04-async-parallel`, `exercise-05-dsa-patterns`. Run: `uv run pytest topics/01-programming-fundamentals/exercises -q`.
- **Interview Q/A (25+):** in `topics/01-programming-fundamentals/interview-questions.md` with one-liner + hook + gotchas + self-score table.
- **Infra fixes:** `pyproject.toml` pytest config kept minimal; exercise tests use unique basenames + importlib loader (no cross-import collision); ruff clean; fixed ESM-`this` demo for `"type": "module"`.
- **Repo reorg:** `01–29` moved under `topics/` + `topics/README.md` index; root `README.md` banner; `docs/conventions.md`, `projects/README.md`, `Makefile`, `.github` templates updated to `topics/...` paths.
- **Verified:** `uv run pytest topics/01-programming-fundamentals/exercises -q` → 12 passed; `ruff check` + `ruff format --check` clean; node examples run (incl. `.ts` via type-stripping).

### 2026-09-30 — 02-api-design-web-protocols ✅
- **Notes (8):** `01-rest-foundations` (restaurant menu, nouns-vs-verbs, safe/idempotent, RMM/HATEOAS), `02-status-errors-versioning` (codes 1xx–5xx, RFC7807, versioning, cursor/keyset, 202+poll), `03-http-deep-dive` (1.1/2/3, anatomy, param seats, content types, streaming), `04-headers-cookies-cors` (20 headers, cookie stamps, preflight checklist), `05-other-styles` (SOAP deed, GraphQL librarian N+1/DataLoader, gRPC walkie-talkie, WS/SSE/webhooks, picker table), `06-caching-rate-limit` (ETag→304, token/leaky/sliding, 429+Retry-After), `07-tooling-middleware` (OpenAPI/AsyncAPI, curl, gateways/BFF, onion chain), `08-resilience` (timeouts, backoff+jitter, breaker, bulkhead, DLQ).
- **Examples (11, all ran green):** `01_rest_design.py`, `02_status_errors_pagination.py` (cursor walk 1→10), `03_caching.py` (200→304), `04_rate_limit_retry.py` (burst+refill, idempotency), `05_circuit_breaker.py` (fuse-box states), `06_styles_compare.py` (N+1 5→1, HMAC), `07_sse_webhooks_cors.py` (live localhost SSE server + client, preflight, cookies), `08_middleware.py` (trace→auth→log), `09_openapi_contract.py` (lint + curl), `10_fetch_client.js` (429→retry w/ Retry-After), `11_sse_parser.js` (tape parser; fixed comment-line bug during verification).
- **Exercises (5, 12/12 pytest pass):** `exercise-01-orders-api-design`, `exercise-02-cursor-pagination`, `exercise-03-etag-cache`, `exercise-04-bucket-backoff`, `exercise-05-breaker-webhook`. Run: `uv run pytest topics/02-api-design-web-protocols/exercises -q`.
- **Interview Q/A (25+):** in `topics/02-api-design-web-protocols/interview-questions.md` with one-liner + hook + gotchas + self-score table.
- **Verified:** 12 passed; `ruff check` + `ruff format --check` clean; node examples run.

### 2026-09-30 — 03-backend-frameworks ✅
- **Stack:** `uv add fastapi sqlalchemy python-multipart pydantic-settings` (TestClient via httpx; `pyproject.toml` + ruff per-file-ignores `B008` for the FastAPI `Depends` idiom).
- **Notes (7):** `01-frameworks-map` (picker + lifecycle), `02-routing-validation-di` (Pydantic guard, response_model, Depends/overrides), `03-orm` (Session basket, N+1 kill, Alembic, repo), `04-async-asgi-servers` (def vs async def, WSGI/ASGI, workers, lifespan, health vs ready), `05-background-tasks` (202+jobs, Celery/RQ/BullMQ/APScheduler, idempotent+DLQ), `06-upload-stream-page` (capped streamed uploads, StreamingResponse, page dep), `07-config-12factor` (env decides, vaults, fail fast, mask).
- **Examples (7, all ran green):** `01_minimal_fastapi.py` (lifespan + 201/422 via TestClient), `02_di_overrides.py` (composed deps + swap), `03_sqlalchemy_nplus1.py` (counter proves 6→2 + repo; fixed missing FK during verification), `04_tasks_queue.py` (202 + idempotent retry worker), `05_upload_stream_page.py` (201 upload + NDJSON 50 lines + page 11–15), `06_config.py` (dev/prod + masked), `07_node_http_api.js` (zero-dep onion).
- **Exercises (5, 10/10 pytest pass):** `exercise-01-crud-api` (TestClient 201/404/422), `exercise-02-pagination-dep`, `exercise-03-repo-n1` (≤2 queries asserted), `exercise-04-job-retry`, `exercise-05-config-stream`. Run: `uv run pytest topics/03-backend-frameworks/exercises -q`.
- **Interview Q/A (20+):** in `topics/03-backend-frameworks/interview-questions.md` + gotchas + self-score table.
- **Verified:** 10 passed; `ruff check` + `ruff format --check` clean; topics 01–02 still green.

### 2026-09-30 — 04-auth-security ✅
- **Stack:** `uv add pyjwt cryptography` (HS256 + RS256 via real RSA keys; TestClient auth API).
- **Notes (8):** `01-authn-authz-models` (gates, badges, MFA/passkeys, SSO/OIDC/SAML/LDAP/Kerberos, IdPs), `02-jwt` (3 parts, HS vs RS, rotation, jti), `03-oauth2-oidc` (grants, PKCE, scopes, sub), `04-access-control` (RBAC/ABAC/ACL, OPA, IDOR), `05-crypto-tls` (hash/enc/encoding, envelope/KMS, handshake, mTLS, LE), `06-owasp` (API 10 + classics thief→lock), `07-app-defenses` (headers/CSP, validation, WAF, SAST/SCA/DAST, audit), `08-privacy-llm-zerotrust` (PII/GDPR, LLM Top 10, zero trust, SOC2/ISO/HIPAA).
- **Examples (8, all ran green):** `01_password_hashing.py` (lint caught real bug: verify ignored stored cost — fixed + iters param), `02_jwt_hs_rs.py` (tamper/expiry/alg-confusion rejected), `03_auth_api.py` (rewrote messy draft → clean login/rotate/logout, 401/403), `04_oauth_pkce.py`, `05_rbac_abac.py`, `06_injection_defenses.py` (fixed Win `echo` → `sys.executable -c`; cleaned SSRF check), `07_security_headers.py`, `08_auth_client.js` (fixed refresh-without-headers crash).
- **Exercises (5, 10/10 pytest pass):** `exercise-01-passwords`, `exercise-02-jwt-rotation`, `exercise-03-idor-guard`, `exercise-04-injection-guards`, `exercise-05-headers-pii`. Run: `uv run pytest topics/04-auth-security/exercises -q`.
- **Interview Q/A (20+):** in `topics/04-auth-security/interview-questions.md` + gotchas + self-score table.
- **Verified:** 10 passed; `ruff check` + `ruff format --check` clean.

### 2026-09-30 — 05-networking-proxy-dns ✅ (`topic/05-networking-proxy-dns` → main)
- **Notes (7):** `01-tcp-ip-foundation` (OSI/TCP-IP, TCP vs UDP, handshake, ports/sockets), `02-subnets-nat-vpc` (CIDR, routing, NAT, SG/NACL/bastion/VPN), `03-dns` (9 records, TTL, resolution, split-horizon, custom domains), `04-proxies` (forward/reverse, nginx 15-liner, corp env/PAC), `05-lb-cdn` (L4 vs L7, 5 algorithms, health/sticky/TLS, edge), `06-tunnels-mesh` (-L/-R/-D/k8s, discovery, Istio/Linkerd), `07-debugging` (symptom→tool table, corporate classics).
- **Examples (7, all ran green on live localhost sockets):** `01_tcp_udp_sockets.py`, `02_cidr_subnets.py` (fixed `in`-needs-ip_address + wrong /26 assert live), `03_dns_cache.py`, `04_reverse_proxy.py` (backend+proxy, XFF/trace asserted), `05_load_balancer.py`, `06_tunnel_cmds.py`, `07_debug_probes.js` (dns+nc+curl timings).
- **Exercises (5, 10/10 pytest pass):** `exercise-01-cidr-plan`, `exercise-02-dns-cache`, `exercise-03-proxy-headers` (fixed dead-upstream times in test), `exercise-04-lb-pickers`, `exercise-05-tunnel-debug`. Run: `uv run pytest topics/05-networking-proxy-dns/exercises -q`.
- **Interview Q/A (20+):** in `topics/05-networking-proxy-dns/interview-questions.md` + gotchas + self-score table.
- **Verified:** 10 passed; `ruff check` + `ruff format --check` clean (fixed RUF059/B905/E501).

### 2026-09-30 — 06-databases ✅ (`topic/06-databases` → main)
- **Notes (8):** `01-sql-core` (DDL/DML/DCL/TCL, joins + LEFT-trap, CTE→window, views/routines), `02-normalization` (1NF→BCNF, denormalize reads), `03-indexes-plans` (B-tree/GIN/partial/covering, EXPLAIN ritual, pgvector pointer), `04-transactions` (ACID, ghosts, MVCC, deadlocks, SKIP LOCKED, PgBouncer), `05-nosql` (5 countries, embed-vs-ref, pipeline, Cassandra keys, ES/BM25), `06-graph` (Cypher, RDF, fraud/recs/GraphRAG), `07-oltp-olap` (counter vs census, columnar, lake/house, JSONB/FTS), `08-distributed-theory` (CAP/PACELC/BASE, sharding, quorum, PITR).
- **Examples (8, sqlite stdlib + node, all green):** `01_ddl_joins_windows.py`, `02_normalization.py`, `03_indexes_explain.py` (SCAN 2.9ms→SEARCH 0.2ms; planner picked composite over partial — re-demoed honestly on amount), `04_transactions.py` (rewrote broken lock-order helper + shared-conn threads → per-thread conns + busy-retry; 20 threads exact), `05_doc_pipeline.py` (removed nonsense assert), `06_bm25_search.py` (math beat my narrative — now teaches saturation + FTS5 agrees), `07_consistent_hash_quorum.py` (27% move), `08_graph_traversal.js`.
- **Exercises (5, 7/7 pytest pass):** `exercise-01-cte-window`, `exercise-02-index-fix`, `exercise-03-transfer`, `exercise-04-pipeline`, `exercise-05-bm25-ring`. Run: `uv run pytest topics/06-databases/exercises -q`.
- **Interview Q/A (20+):** in `topics/06-databases/interview-questions.md` + gotchas + self-score table.
- **Verified:** 7 passed; `ruff check` + `ruff format --check` clean (SIM105 suppress adopted).

### 2026-09-30 — 07-caching ✅ (`topic/07-caching` → main)
- **Stack:** `uv add fakeredis cachetools` (real Redis commands offline; Lua documented as prod script — fakeredis verified unable).
- **Notes (6):** `01-strategies` (5 habits, delete-not-update, TTL), `02-eviction-horsemen` (LRU/LFU/FIFO/TTL + 4 shields), `03-redis-types` (9 types + pub/sub + MULTI/Lua), `04-redis-ops` (RDB/AOF, Sentinel/Cluster/slots, Redlock+fencing, limits/sessions, Stack), `05-python-layers` (lru_cache/TTLCache, memcached, L1→DB cake), `06-llm-caching` (exact/semantic, prompt cache, KV math).
- **Examples (8, all green):** `01_strategies.py`, `02_eviction.py`, `03_singleflight.py` (20 threads → 1 trip), `04_redis_types.py` (all 9 types + pubsub + MULTI), `05_lock_limit.py` (token lock + zset window), `06_python_cache.py`, `07_semantic_cache.py` (paraphrase 0.90 hit + 10.7GB KV math), `08_http_cache.js` (live 200→304).
- **Exercises (5, 9/9 pytest pass):** `exercise-01-aside-ttl`, `exercise-02-lru`, `exercise-03-singleflight` (cleaned thread-lambda leftover in test), `exercise-04-leaderboard-lock`, `exercise-05-semantic`. Run: `uv run pytest topics/07-caching/exercises -q`.
- **Interview Q/A (20+):** in `topics/07-caching/interview-questions.md` + gotchas + self-score table.
- **Verified:** 9 passed; `ruff check` + `ruff format --check` clean.

### 2026-09-30 — 08-messaging-async ✅ (`topic/08-messaging-async` → main)
- **Notes (7):** `01-queues-streams` (compete/broadcast/replay, SNS→SQS, backpressure), `02-kafka` (partitions/groups/offsets, retention/compaction, EOS, RF=3), `03-rabbitmq` (4 exchanges, ack/prefetch/quorum), `04-semantics` (3 promises, idempotency, DLQ, ordering), `05-eda-patterns` (sourcing/CQRS/saga/outbox), `06-processing` (Kappa, windows, Spark/Flink), `07-orchestration` (4 conductors + GenAI plays).
- **Examples (8, all green):** `01_queue_vs_stream.py`, `02_kafka_sim.py`, `03_rabbitmq_sim.py`, `04_semantics_dlq.py` (fixed attempt-counter bug live), `05_saga_outbox.py`, `06_redis_streams.py` (real XADD/groups/PEL on fakeredis), `07_sourcing_cqrs.py`, `08_dag_runner.js` (chunk retried try2).
- **Exercises (5, 9/9 pytest pass):** `exercise-01-partitions`, `exercise-02-topic-route` (mid-`#` recursion), `exercise-03-idempotent-dlq`, `exercise-04-saga`, `exercise-05-sourced-account`. Run: `uv run pytest topics/08-messaging-async/exercises -q`.
- **Interview Q/A (20+):** in `topics/08-messaging-async/interview-questions.md` + gotchas + self-score table.
- **Verified:** 9 passed; `ruff check` + `ruff format --check` clean (B007/SIM105/RUF017 fixed).


## Documentation pass — 2026-10-01

The topic material now follows a consistent learning pattern: **explanation → examples/practice → exercises → interview questions**. Topics 09–29 received expanded Markdown explanations and dedicated `practice.md` guides. Topics 01–08 already contained substantial explanatory notes and existing runnable practice, so those materials were preserved rather than replaced.

> Note: this documentation pass does **not** mark a topic complete. Completion still requires running the examples, finishing exercises, and revising the interview Q&A as recorded above.
