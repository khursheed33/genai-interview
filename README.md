# Full Stack GenAI Developer (4-5 YOE): Topic Checklist

> **Repo layout:** practice content lives in [`topics/`](./topics/) (01–29, see [`topics/README.md`](./topics/README.md)), progress in [`docs/progress-tracker.md`](./docs/progress-tracker.md), end-to-end builds in [`projects/`](./projects/). Setup: `scripts/setup.ps1` (Windows) or `scripts/setup.sh` + `make up`.

## 1. Programming Fundamentals
**Python**
- Data types, mutability, comprehensions, generators, iterators, decorators, context managers
- OOP, dunder methods, dataclasses, Pydantic, typing/type hints
- Async: asyncio, async/await, event loop, threads vs processes, GIL, multiprocessing
- Virtual envs, pip/poetry/uv, packaging, requirements management
- Exception handling, custom exceptions, logging module
- Memory management, garbage collection, profiling

**JavaScript / TypeScript / Node.js**
- Closures, prototypes, `this`, hoisting, event loop, promises, async/await
- ES6+ features, modules (CJS vs ESM), TypeScript generics/interfaces/utility types
- Node internals: event loop phases, streams, buffers, worker threads, clustering
- npm/yarn/pnpm, package.json, semantic versioning

**Core CS**
- DSA basics: arrays, hashmaps, trees, graphs, heaps, sorting, searching, two pointers, sliding window, recursion, DP basics
- Big-O complexity
- SOLID, DRY, KISS, YAGNI
- Design patterns: Singleton, Factory, Builder, Adapter, Decorator, Strategy, Observer, Repository, Dependency Injection
- Concurrency: race conditions, deadlocks, locks, semaphores, thread safety

## 2. API Design & Web Protocols
**REST**
- Principles, constraints, resource modeling, naming conventions
- HTTP methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- Idempotency, safe methods
- Status codes (1xx-5xx), error response design
- Versioning strategies, pagination (offset, cursor, keyset), filtering, sorting
- HATEOAS, Richardson Maturity Model
- Content negotiation, HTTP caching (ETag, Cache-Control, Last-Modified)
- Rate limiting, throttling, quotas, backpressure
- Bulk operations, partial responses, long-running operations, async APIs, polling

**Other API styles**
- SOAP: WSDL, XSD, envelope, header, body, fault, WS-Security
- GraphQL: schema, queries, mutations, subscriptions, resolvers, N+1, DataLoader, federation
- gRPC: protobuf, unary/streaming, HTTP/2
- WebSockets, Server-Sent Events (SSE), long polling, webhooks
- tRPC, JSON-RPC
- REST vs SOAP vs GraphQL vs gRPC: trade-offs

**HTTP deep dive**
- HTTP/1.1 vs 2 vs 3 (QUIC), keep-alive, multiplexing
- Request/response anatomy
- Headers: Authorization, Content-Type, Accept, Cache-Control, ETag, CORS headers, Cookie/Set-Cookie, User-Agent, Origin, Referer, Host, X-Forwarded-For/Proto, X-Request-ID, Retry-After, Content-Security-Policy, HSTS, X-Frame-Options, X-Content-Type-Options, Transfer-Encoding, Content-Encoding
- Query params vs path params vs body vs headers
- Content types: JSON, form-data, x-www-form-urlencoded, multipart, binary, NDJSON
- Cookies: SameSite, HttpOnly, Secure
- CORS, preflight
- Compression (gzip, brotli), chunked transfer, streaming responses

**API tooling**
- OpenAPI/Swagger, AsyncAPI, Postman, Insomnia, curl, HTTPie
- API gateways, API contracts, mock servers
- SDK generation, API documentation

**Interceptors / Middleware**
- Request/response interceptors (Axios, Angular, FastAPI, Express, Spring)
- Middleware chain, filters, guards, pipes
- Use cases: auth, logging, retries, error handling, correlation IDs

**Resilience patterns**
- Retries with exponential backoff and jitter, timeouts
- Circuit breaker, bulkhead, fallback, idempotency keys
- Graceful degradation, dead letter queues

## 3. Backend Frameworks
- FastAPI, Flask, Django (DRF); Node/Express/NestJS
- Dependency injection, routing, validation, serialization
- ORM: SQLAlchemy, Prisma, TypeORM, Sequelize
- Background tasks: Celery, RQ, BullMQ, Dramatiq, APScheduler
- Sync vs async endpoints, ASGI vs WSGI, Uvicorn/Gunicorn/Hypercorn workers
- File uploads, streaming, pagination, lifespan events
- Config management: env vars, .env, secrets, 12-factor app

## 4. Authentication, Authorization & Security
- AuthN vs AuthZ
- Basic, API key, Bearer, session-based, token-based
- JWT: structure, signing (HS256/RS256), expiry, refresh tokens, revocation
- OAuth 2.0: grant types (auth code, PKCE, client credentials, device), scopes
- OpenID Connect, SAML, SSO, LDAP, Kerberos
- MFA, passwordless, RBAC, ABAC, ACL, policy engines (OPA)
- Keycloak, Auth0, Okta, Azure AD/Entra, Cognito
- mTLS, TLS/SSL handshake, certificates, CA, cert chain, Let's Encrypt
- Hashing vs encryption vs encoding, salting, bcrypt/argon2
- Symmetric vs asymmetric encryption, key management, KMS, HSM
- Secrets management: Vault, AWS Secrets Manager, Key Vault
- OWASP Top 10, OWASP API Top 10, OWASP LLM Top 10
- SQL injection, XSS, CSRF, SSRF, XXE, IDOR, path traversal, clickjacking
- Input validation, output encoding, sanitization
- CORS misconfig, security headers, CSP
- Rate limiting, DDoS protection, WAF, bot protection
- Dependency scanning, SAST/DAST, SCA, container scanning
- PII handling, GDPR, data masking, encryption at rest/in transit
- Audit logging, compliance (SOC2, ISO 27001, HIPAA)
- Zero trust

## 5. Networking, Proxy, DNS
- OSI/TCP-IP model, TCP vs UDP, 3-way handshake, ports, sockets
- IP, CIDR, subnets, NAT, gateways, routing
- DNS: records (A, AAAA, CNAME, MX, TXT, NS, SRV, PTR), TTL, resolution flow, recursive vs authoritative, DNS caching, split-horizon DNS
- Local DNS mapping: /etc/hosts, hosts file, dnsmasq, CoreDNS, Route53, Cloudflare
- Domain mapping, subdomains, wildcard, custom domain setup, SSL binding
- Forward proxy vs reverse proxy, transparent proxy
- Nginx, HAProxy, Traefik, Envoy, Apache: config, upstreams, location blocks, rewrites, redirects, proxy_pass, headers
- Corporate proxy config: HTTP_PROXY/HTTPS_PROXY/NO_PROXY, PAC files, proxy auth
- Load balancing: L4 vs L7, algorithms (round robin, least connections, IP hash), health checks, sticky sessions, SSL termination/offloading
- CDN: Cloudflare, CloudFront, edge caching, cache invalidation
- VPN, VPC, subnets, security groups, NACLs, firewalls, bastion hosts
- Port forwarding, SSH tunneling
- Service discovery, service mesh (Istio, Linkerd)
- Debugging tools: ping, traceroute, nslookup, dig, curl -v, netstat/ss, tcpdump, Wireshark, telnet/nc, openssl s_client

## 6. Databases
**SQL (RDBMS)**
- PostgreSQL, MySQL, SQL Server, Oracle basics
- DDL/DML/DCL/TCL, joins, subqueries, CTEs, window functions, aggregations, views, materialized views
- Stored procedures, triggers, functions
- Normalization (1NF to BCNF), denormalization
- Indexes: B-tree, hash, GIN/GiST, composite, covering, partial; query plans (EXPLAIN)
- Transactions, ACID, isolation levels, locking, MVCC, deadlocks
- Connection pooling (PgBouncer), migrations (Alembic, Flyway, Prisma)
- Replication, sharding, partitioning, read replicas, failover
- Query optimization, slow query analysis, N+1 problem
- pgvector, JSONB, full-text search

**NoSQL**
- Types: document, key-value, wide-column, graph, time-series, search
- MongoDB: documents, aggregation pipeline, indexes, sharding, replica sets, schema design (embed vs reference)
- Cassandra/DynamoDB: partition keys, data modeling, consistency levels, GSI/LSI
- Elasticsearch/OpenSearch: inverted index, analyzers, BM25, mappings, queries
- Firestore, CouchDB, Cosmos DB

**Graph Databases**
- Neo4j: property graph model, Cypher, nodes, relationships, traversals
- RDF, SPARQL, triple stores
- Use cases: knowledge graphs, fraud detection, recommendations
- Gremlin, Amazon Neptune, ArangoDB, Memgraph

**Time-series / Analytical**
- InfluxDB, TimescaleDB, ClickHouse, BigQuery, Snowflake, Redshift
- OLTP vs OLAP, data warehouse vs data lake vs lakehouse

**Theory**
- CAP theorem, PACELC, BASE, eventual vs strong consistency
- SQL vs NoSQL selection criteria
- Sharding strategies, consistent hashing, replication topologies, quorum
- Polyglot persistence
- Backup/restore, PITR, data retention

## 7. Caching
- Cache strategies: cache-aside, read-through, write-through, write-behind, refresh-ahead
- Eviction: LRU, LFU, FIFO, TTL
- Cache invalidation, stampede/thundering herd, penetration, avalanche, hot keys
- Redis: data types (string, hash, list, set, sorted set, bitmap, HyperLogLog, streams, geo), pub/sub, transactions, Lua scripts
- Redis persistence (RDB, AOF), replication, Sentinel, Cluster, eviction policies
- Distributed locks (Redlock), rate limiting with Redis, session store
- Redis Stack: RediSearch, RedisJSON, vector search
- Memcached, in-memory caching (functools.lru_cache, cachetools)
- Browser cache, CDN cache, HTTP cache, application cache, DB cache
- Semantic caching for LLMs, prompt caching, KV cache

## 8. Messaging & Async Processing
- Message queues vs event streaming, pub/sub
- Kafka: topics, partitions, consumer groups, offsets, retention, exactly-once, compaction
- RabbitMQ: exchanges, queues, routing, acks
- AWS SQS/SNS/EventBridge, Azure Service Bus, Google Pub/Sub, NATS, Redis Streams
- Delivery semantics: at-most/at-least/exactly-once
- Idempotent consumers, DLQ, retries, ordering, backpressure
- Event-driven architecture, event sourcing, CQRS, saga pattern, outbox pattern
- Batch vs stream processing, Spark, Flink basics
- Workflow orchestration: Airflow, Temporal, Prefect, Step Functions

## 9. System Design
**Fundamentals**
- Scalability: vertical vs horizontal, stateless vs stateful
- Latency vs throughput, availability, reliability, durability, SLA/SLO/SLI
- Back-of-envelope estimation, capacity planning
- Load balancing, caching, CDN, sharding, replication
- Consistent hashing, bloom filters, rate limiter algorithms (token bucket, leaky bucket, sliding window)
- Idempotency, distributed transactions, 2PC, saga
- Leader election, consensus (Raft, Paxos), distributed locks, gossip
- Failure modes, disaster recovery, RPO/RTO, multi-region, active-active/passive
- Data partitioning, hot spots

**Classic design problems**
- URL shortener, rate limiter, notification system, chat app, news feed, file storage, search autocomplete, web crawler, payment system, video streaming, ride sharing, distributed cache, job scheduler, API gateway

**GenAI system designs**
- RAG chatbot at scale, enterprise document Q&A, multi-tenant LLM platform, AI agent platform, semantic search, code assistant, LLM gateway, real-time voice assistant, document processing pipeline (OCR + LLM), recommendation with embeddings, multi-agent workflow system

**Documentation**
- HLD vs LLD, UML, sequence/class/ER diagrams, C4 model
- ADRs (Architecture Decision Records)

## 10. Software Architecture
- Monolith vs modular monolith vs microservices vs serverless
- Layered, hexagonal (ports and adapters), clean architecture, onion, DDD (bounded contexts, aggregates, entities, value objects)
- Event-driven, CQRS, event sourcing
- BFF (Backend for Frontend), API gateway, strangler fig, sidecar, ambassador
- Service-to-service communication: sync vs async
- Service registry/discovery, config server
- Multi-tenancy patterns
- Monorepo vs polyrepo
- Feature flags, blue-green, canary, rolling deployments
- Twelve-factor app
- Distributed tracing, correlation IDs
- Technical debt, refactoring, backward compatibility

## 11. Frontend (Full Stack)
- HTML5, CSS3, Flexbox, Grid, responsive design, accessibility (a11y, ARIA)
- React: hooks, context, reducers, memoization, lifecycle, reconciliation, virtual DOM, suspense, error boundaries
- Next.js: SSR, SSG, ISR, App Router, server components, API routes, streaming
- State management: Redux, Zustand, Recoil, React Query/TanStack Query
- Angular/Vue basics (if applicable)
- Forms, validation, routing
- Streaming UI for LLMs: SSE, WebSockets, token streaming, markdown rendering, optimistic updates
- Chat UI patterns, file upload, citations display, feedback (thumbs up/down)
- Vercel AI SDK, CopilotKit, Streamlit, Gradio, Chainlit
- Performance: lazy loading, code splitting, bundle optimization, Core Web Vitals, caching
- Browser storage: localStorage, sessionStorage, IndexedDB, cookies
- Web security: XSS, CSP, CORS
- Build tools: Webpack, Vite, Babel
- Testing: Jest, React Testing Library, Cypress, Playwright

## 12. DevOps, Deployment & Cloud
**Docker**
- Images, containers, layers, Dockerfile instructions, multi-stage builds, caching, .dockerignore
- CMD vs ENTRYPOINT, COPY vs ADD, ARG vs ENV
- Volumes, bind mounts, networks (bridge, host, overlay), port mapping
- Docker Compose, healthchecks, restart policies
- Registries (Docker Hub, ECR, ACR, GCR), image tagging, scanning
- Image size optimization, non-root users, distroless/alpine
- Container debugging: logs, exec, inspect, stats
- GPU containers, NVIDIA container toolkit

**Kubernetes**
- Pods, Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs/CronJobs
- Services (ClusterIP, NodePort, LoadBalancer), Ingress, Ingress controllers
- ConfigMaps, Secrets, PV/PVC, StorageClasses
- Namespaces, RBAC, ServiceAccounts, network policies
- HPA, VPA, cluster autoscaler, KEDA
- Probes (liveness, readiness, startup), resource requests/limits
- Helm, Kustomize, operators, CRDs
- kubectl commands, troubleshooting (CrashLoopBackOff, ImagePullBackOff, OOMKilled)
- Managed: EKS, AKS, GKE; OpenShift

**CI/CD**
- GitHub Actions, GitLab CI, Jenkins, Azure DevOps, CircleCI, ArgoCD/FluxCD (GitOps)
- Pipeline stages: build, test, scan, package, deploy
- Deployment strategies: rolling, blue-green, canary, recreate, shadow
- Environments (dev/staging/prod), promotion, rollbacks
- Artifact management, semantic versioning, release management
- Git: branching strategies (GitFlow, trunk-based), rebase vs merge, cherry-pick, stash, bisect, hooks, PR/code review practices

**Infrastructure as Code**
- Terraform (state, modules, providers), Pulumi, CloudFormation, Bicep, Ansible

**Cloud (AWS/Azure/GCP; know at least one deeply)**
- Compute: EC2, Lambda, ECS/Fargate, App Service, Cloud Run
- Storage: S3/Blob/GCS, EBS, EFS
- Databases: RDS, DynamoDB, Aurora, Cosmos DB
- Networking: VPC, subnets, security groups, Route53, ALB/NLB, API Gateway, CloudFront
- IAM, roles, policies, managed identities
- Serverless: Lambda, Step Functions, EventBridge
- Cost management, tagging, budgets
- Well-Architected Framework
- Cloud AI services: Bedrock, SageMaker, Azure OpenAI/AI Foundry/AI Search, Vertex AI

**Web servers**
- Nginx/Apache config, Gunicorn/Uvicorn, PM2, systemd services, supervisord
- SSL/TLS setup, certbot

**Environment mgmt**
- Environment variables, config per env, secrets injection, feature flags

## 13. Scripting & Linux
- Bash: variables, conditionals, loops, functions, pipes, redirection, exit codes, cron, `set -euo pipefail`
- Text tools: grep, sed, awk, cut, sort, uniq, xargs, find, jq, yq
- File permissions, users/groups, chmod/chown, umask
- Process mgmt: ps, top/htop, kill, nohup, systemctl, journalctl
- Disk/memory/network: df, du, free, lsof, iostat, vmstat
- SSH, scp, rsync, ssh keys, config
- Python scripting, PowerShell basics
- Makefiles, task runners
- Automation: cron, systemd timers, Ansible

## 14. Logging, Monitoring & Observability
- Three pillars: logs, metrics, traces
- Log levels, structured (JSON) logging, correlation/trace IDs, log rotation, sensitive data masking
- Centralized logging: ELK/EFK, Loki, Splunk, CloudWatch, Datadog, Azure Monitor
- Metrics: Prometheus, Grafana, StatsD, RED/USE/Golden signals
- Tracing: OpenTelemetry, Jaeger, Zipkin
- APM tools: New Relic, Datadog, Dynatrace, Sentry
- Alerting, SLOs, error budgets, on-call, incident management, RCA/postmortems
- Health endpoints, uptime monitoring
- Profiling, load testing (Locust, k6, JMeter)
- **LLM observability:** LangSmith, Langfuse, Arize Phoenix, Helicone, Weights & Biases, traces per LLM call, token/cost/latency tracking

## 15. Testing & Quality
- Unit, integration, E2E, contract, smoke, regression, load, stress, chaos testing
- Test pyramid, TDD, BDD
- pytest, unittest, Jest, mocking, stubbing, fixtures, parametrization, coverage
- Contract testing (Pact), API testing (Postman/Newman, REST Assured)
- Test data management, test containers
- Code quality: linting (ruff, flake8, ESLint), formatters (black, prettier), type checkers (mypy), pre-commit, SonarQube
- Code reviews, documentation standards
- **Testing LLM apps:** non-determinism, mocking LLMs, golden datasets, regression evals

## 16. GenAI: LLM Fundamentals
- Transformer architecture, attention, self-attention, multi-head attention, positional encoding
- Encoder-only vs decoder-only vs encoder-decoder (BERT, GPT, T5)
- Pretraining, fine-tuning, RLHF, DPO, instruction tuning
- Tokens, tokenization (BPE, WordPiece, SentencePiece), tokenizers (tiktoken)
- Context window, max tokens, input vs output tokens, context length limits
- Sampling parameters: temperature, top-p, top-k, frequency/presence penalty, stop sequences, seed
- Greedy vs beam search, logprobs
- Hallucination: types, causes, mitigation
- Model types: base, chat/instruct, reasoning models, multimodal, small language models, MoE
- Open vs closed models: GPT, Claude, Gemini, Llama, Mistral, Qwen, DeepSeek, Gemma, Phi
- Model selection criteria: cost, latency, quality, context size, licensing, privacy
- Quantization (INT8/INT4, GGUF, GPTQ, AWQ), distillation, pruning
- Scaling laws, emergent abilities, knowledge cutoff
- Structured outputs, JSON mode, function calling, constrained decoding
- Streaming responses, batch APIs
- LLM APIs: OpenAI, Anthropic, Azure OpenAI, Google, Bedrock, Hugging Face, Ollama, OpenRouter

## 17. Prompt Engineering
- System vs user vs assistant roles, prompt structure
- Zero-shot, one-shot, few-shot, in-context learning
- Chain-of-Thought, zero-shot CoT, self-consistency, Tree-of-Thought, ReAct, Reflexion, least-to-most, step-back prompting
- Role prompting, persona, delimiters, XML tags, output format specification
- Prompt templates, variables, prompt chaining, meta-prompting
- Negative prompting, instruction hierarchy
- Prompt versioning, management, registries, A/B testing
- Prompt optimization: DSPy, automatic prompt tuning
- Prompt injection (direct/indirect), jailbreaks, prompt leaking, defenses
- Context engineering: what to include, ordering, compression, summarization
- Prompt caching, token optimization
- Handling long context: lost-in-the-middle, chunking, map-reduce, refine

## 18. Embeddings & Vector Databases
**Embeddings**
- What embeddings are, dense vs sparse, semantic similarity
- Embedding models: OpenAI, Cohere, Voyage, BGE, E5, Sentence-Transformers, Gemini, Nomic
- Dimensions, Matryoshka embeddings, normalization
- Similarity metrics: cosine, dot product, Euclidean, Manhattan
- Multimodal embeddings (CLIP), fine-tuning embeddings, domain adaptation
- MTEB benchmark, choosing embedding models

**Vector DBs**
- Pinecone, Weaviate, Qdrant, Milvus, Chroma, FAISS, pgvector, Redis Vector, Elasticsearch/OpenSearch kNN, Azure AI Search, MongoDB Atlas Vector Search, LanceDB
- ANN algorithms: HNSW, IVF, IVF-PQ, LSH, ScaNN, DiskANN
- Exact (kNN) vs approximate (ANN), recall vs latency trade-off
- Index params (M, efConstruction, efSearch, nlist, nprobe)
- Metadata filtering (pre-filter vs post-filter), namespaces, multi-tenancy
- Hybrid search: BM25 + dense, sparse vectors (SPLADE), RRF (Reciprocal Rank Fusion)
- Upserts, deletes, versioning, re-indexing, sharding, scaling
- Quantization in vector DBs, storage cost
- Vector DB vs traditional DB, when to use which

## 19. RAG (Retrieval-Augmented Generation)
- RAG vs fine-tuning vs long-context
- Ingestion pipeline: loaders, parsing (PDF, DOCX, HTML, tables, images), OCR, cleaning
- Chunking: fixed, recursive, semantic, sentence, document-structure-aware, parent-child, sliding window, overlap
- Metadata enrichment, indexing strategies
- Retrieval: dense, sparse, hybrid, multi-vector, ColBERT
- Query transformation: rewriting, expansion, HyDE, multi-query, decomposition, step-back
- Reranking: cross-encoders, Cohere Rerank, bge-reranker, LLM reranking
- MMR (diversity), top-k tuning, similarity thresholds
- Context assembly, compression, citation/attribution, source grounding
- Advanced RAG: Self-RAG, Corrective RAG (CRAG), Adaptive RAG, Agentic RAG, GraphRAG, multi-hop, RAPTOR, Speculative RAG
- Modular RAG, multimodal RAG
- Conversational RAG: chat history, query condensation, memory
- Text-to-SQL, text-to-Cypher, structured data RAG
- Knowledge graphs + LLM
- Freshness, incremental updates, deletions, access control in RAG (document-level security)
- RAG failure modes: retrieval misses, wrong chunks, stale data, context overflow
- Caching in RAG

## 20. Agents & Orchestration
**Concepts**
- LLM chains vs agents (deterministic workflow vs autonomous)
- Workflows vs agents (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)
- Agent loop: perceive, plan, act, observe
- Agent patterns: ReAct, Plan-and-Execute, Reflection, Tool-use, ReWOO, LATS
- Single-agent vs multi-agent; supervisor, hierarchical, swarm/handoff, collaborative, debate
- Planning, task decomposition, self-correction
- Autonomy levels, human-in-the-loop, approval gates
- When NOT to use agents; reliability/cost/latency trade-offs

**Memory**
- Short-term (context/buffer/summary) vs long-term (vector, KV, graph)
- Episodic, semantic, procedural memory
- Memory frameworks: Mem0, Zep, LangMem
- Checkpointing, thread state, persistence

**Tools / Function Calling**
- Tool schemas (JSON schema), tool selection, parallel tool calls
- Tool design principles: naming, descriptions, error messages, idempotency
- Tool result handling, retries, validation
- Code interpreter, web search, browser use, computer use
- Tool authorization and sandboxing

**Frameworks**
- LangChain: LCEL, Runnables, prompt templates, output parsers, retrievers, chains, callbacks, document loaders, text splitters
- **LangGraph:** StateGraph, nodes, edges, conditional edges, state/reducers, checkpointers, persistence, interrupts (human-in-the-loop), subgraphs, streaming, time travel, Send API (map-reduce), LangGraph Platform/Studio
- LlamaIndex: indices, query engines, agents, workflows
- CrewAI, AutoGen/AG2, Semantic Kernel, Haystack, Pydantic AI, OpenAI Agents SDK, Claude Agent SDK, Google ADK, smolagents, DSPy, Agno
- Framework comparison and when to go framework-less

**MCP (Model Context Protocol)**
- Architecture: host, client, server
- Primitives: tools, resources, prompts, sampling, roots, elicitation
- Transports: stdio, SSE, streamable HTTP
- Building MCP servers/clients (Python/TS SDKs)
- MCP auth (OAuth), security considerations, tool poisoning
- MCP vs function calling vs REST/OpenAPI
- MCP gateways, registries

**Agent interoperability**
- A2A (Agent-to-Agent) protocol, ACP, agent cards
- Agent-to-UI protocols (AG-UI)
- Skills, subagents

**Agent challenges**
- Infinite loops, cost blowup, tool misuse, error recovery, state management, non-determinism, latency
- Guardrails for agents, sandboxing, permissions, least privilege

## 21. Evaluation
- Why LLM eval is hard; offline vs online evaluation
- Ground truth / golden datasets: creation, annotation, synthetic data generation, dataset versioning, edge cases, adversarial sets
- Reference-based vs reference-free evaluation
- Classic metrics: accuracy, precision, recall, F1, BLEU, ROUGE, METEOR, BERTScore, perplexity, exact match
- Retrieval metrics: Recall@k, Precision@k, MRR, NDCG, MAP, Hit Rate
- RAG metrics: faithfulness/groundedness, answer relevancy, context precision, context recall, context relevance, answer correctness, hallucination rate
- LLM-as-a-judge: rubrics, pairwise vs pointwise, position/verbosity/self-preference bias, calibration, judge model selection, G-Eval
- Human evaluation, annotation guidelines, inter-annotator agreement
- Agent evaluation: task success, trajectory evaluation, tool-call accuracy, step efficiency, cost per task
- Safety evals: toxicity, bias, PII leakage, jailbreak robustness, red teaming
- Benchmarks: MMLU, HumanEval, GSM8K, MT-Bench, LMSYS Arena, SWE-bench, BEIR, HELM
- Frameworks: RAGAS, DeepEval, TruLens, LangSmith evals, Promptfoo, Arize Phoenix, OpenAI Evals, Langfuse, Giskard, Braintrust
- Regression testing, CI-integrated evals, A/B testing, shadow testing
- Online metrics: user feedback, thumbs up/down, acceptance rate, escalation rate, latency, cost
- Drift monitoring, feedback loops, continuous improvement

## 22. Fine-Tuning & Model Customization
- When to fine-tune vs prompt vs RAG
- SFT, instruction tuning, RLHF, RLAIF, DPO, ORPO, GRPO
- PEFT: LoRA, QLoRA, adapters, prefix tuning, prompt tuning
- Dataset preparation, formats (JSONL, ChatML, Alpaca), data quality, deduplication
- Hugging Face: Transformers, Datasets, PEFT, TRL, Accelerate, Trainer
- Training infra: GPUs, mixed precision, gradient checkpointing, DeepSpeed, FSDP
- Catastrophic forgetting, overfitting, evaluation post-fine-tune
- Merging models, distillation, synthetic data
- Vendor fine-tuning (OpenAI, Bedrock, Vertex, Azure)

## 23. LLM Serving, Inference & LLMOps
- Inference engines: vLLM, TGI, TensorRT-LLM, llama.cpp, Ollama, SGLang, Triton
- Batching (continuous batching), KV cache, PagedAttention, speculative decoding, flash attention
- Latency metrics: TTFT, TPOT, throughput (tokens/sec)
- GPU basics: VRAM sizing, tensor/pipeline parallelism, CPU vs GPU inference
- Model hosting: SageMaker, Azure ML, Vertex, Hugging Face Inference, Modal, Replicate, Together, Groq, Fireworks
- LLM gateways/proxies: LiteLLM, Portkey, Kong AI Gateway, Azure APIM for AI, Cloudflare AI Gateway
- Routing, fallbacks, load balancing across models/providers, retries
- Rate limits (RPM/TPM), quota management, provisioned throughput
- Cost optimization: model routing, caching, prompt compression, smaller models, batching, token budgeting
- Semantic caching (GPTCache, Redis)
- Model/prompt versioning, registries (MLflow), experiment tracking
- CI/CD for LLM apps, canary prompts/models
- Multi-tenancy, per-user cost tracking, usage metering
- Async processing for long LLM jobs, queues, streaming endpoints
- Deprecation handling, vendor lock-in mitigation

## 24. Guardrails, Safety & Responsible AI
- Input/output guardrails, content moderation, topic restriction
- Guardrails frameworks: NeMo Guardrails, Guardrails AI, LLM Guard, Llama Guard, Azure Content Safety, Bedrock Guardrails
- Prompt injection, indirect injection, data exfiltration, jailbreaks, excessive agency
- OWASP LLM Top 10
- PII detection/redaction (Presidio), data privacy, data residency
- Output validation: schema validation, Pydantic, Instructor, retries on parse failure
- Hallucination mitigation: grounding, citations, confidence, abstention
- Bias, fairness, explainability, transparency
- Red teaming, adversarial testing
- Access control on retrieved data, tenant isolation
- Regulations: EU AI Act, GDPR, NIST AI RMF, model cards, AI governance
- Copyright, licensing, IP concerns
- Enterprise concerns: on-prem/private deployments, VPC endpoints, no-training-on-data policies

## 25. Multimodal & Other GenAI Topics
- Vision-language models, image understanding, OCR, document AI (Textract, Document Intelligence, Unstructured, LlamaParse, Docling)
- Speech: STT (Whisper), TTS, real-time voice agents, streaming audio, WebRTC
- Image generation: diffusion basics, Stable Diffusion, DALL·E, Midjourney, ComfyUI
- Video generation basics
- Code generation & assistants, AI coding agents (Copilot, Cursor, Claude Code), sandboxed code execution
- Structured data extraction, classification, summarization, translation pipelines
- Text-to-SQL, NL interfaces to data, analytics agents
- Reasoning models, test-time compute, extended thinking
- Computer use / browser agents
- Small on-device models, edge AI
- Synthetic data generation

## 26. Data Engineering for GenAI
- ETL/ELT, data pipelines, Airflow/dbt
- Data quality, cleaning, deduplication, PII scrubbing
- Document parsing pipelines, OCR, layout analysis
- Data lakes, object storage, parquet/avro/JSON/CSV
- Pandas, NumPy, Polars basics
- Streaming ingestion, CDC, incremental indexing
- Knowledge base management, metadata schemas, taxonomy/ontology
- Data versioning (DVC), lineage, governance
- Search fundamentals: TF-IDF, BM25, inverted index, analyzers

## 27. Classical ML/AI Basics (Expected Awareness)
- Supervised vs unsupervised vs reinforcement learning
- Overfitting, bias-variance, train/val/test split, cross-validation
- Common algorithms: linear/logistic regression, decision trees, random forests, XGBoost, SVM, k-means, PCA
- Neural networks basics, backpropagation, activation functions, loss functions, optimizers
- CNN, RNN, LSTM, GRU → Transformers evolution
- NLP basics: tokenization, stemming, lemmatization, NER, POS, TF-IDF, Word2Vec, GloVe
- Metrics: confusion matrix, ROC-AUC
- MLOps basics: feature stores, model registry, drift, retraining

## 28. Engineering Practices & Soft Skills
- Agile/Scrum/Kanban, sprint planning, estimation, JIRA
- Code review, mentoring juniors, technical documentation, design docs/RFCs
- Requirement gathering, stakeholder communication, translating business needs to AI solutions
- Setting realistic expectations for AI (accuracy, cost, latency)
- POC → production journey, productionizing GenAI apps
- Build vs buy decisions, vendor evaluation
- ROI/cost estimation for LLM apps
- Trade-off analysis and decision-making
- Incident handling, debugging production issues, RCA
- Ownership, cross-team collaboration
- Behavioral (STAR): conflict, failure, leadership, deadlines, ambiguity
- Staying current: papers, newsletters, communities

## 29. Common Interview "Scenario" Themes
- Debugging slow RAG / poor retrieval / hallucinations
- Reducing LLM cost and latency
- Handling rate limits and provider outages
- Scaling from 100 to 1M users
- Securing an LLM app (prompt injection, data leaks)
- Multi-tenant RAG with access control
- Migrating a monolith to microservices
- Zero-downtime deployment
- Handling large documents/files
- Choosing between chain, agent, and multi-agent
- Designing evaluation for a new GenAI feature
- Production incident: API timeouts, memory leaks, high CPU
- Data privacy in regulated industries
- Corporate network issues (proxy, SSL cert errors, DNS)