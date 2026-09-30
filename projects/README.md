# Projects

Small end-to-end builds that combine topics. Suggested order:

1. `rag-chatbot/` — [`topics/06-databases`](../topics/06-databases/) + [`18-embeddings-vector-db`](../topics/18-embeddings-vector-db/) + [`19-rag`](../topics/19-rag/) + [`21-evaluation`](../topics/21-evaluation/) + [`24-guardrails-safety`](../topics/24-guardrails-safety/) (pgvector/Qdrant, evals, guardrails)
2. `agent-assistant/` — [`20-agents-orchestration`](../topics/20-agents-orchestration/) + [`17-prompt-engineering`](../topics/17-prompt-engineering/) + [`21-evaluation`](../topics/21-evaluation/) (LangGraph, tools, MCP, trajectory eval)
3. `llm-gateway/` — [`02-api-design-web-protocols`](../topics/02-api-design-web-protocols/) + [`09-system-design`](../topics/09-system-design/) + [`23-llm-serving-llmops`](../topics/23-llm-serving-llmops/) (rate limits, routing/fallbacks, cost tracking)
4. `doc-pipeline/` — [`26-data-engineering-genai`](../topics/26-data-engineering-genai/) + [`25-multimodal-genai`](../topics/25-multimodal-genai/) + [`19-rag`](../topics/19-rag/) (parse/OCR → chunk → index)

Each project: `README.md` (problem, architecture diagram, API, evals, cost/latency notes) + `src/` + `tests/`.
