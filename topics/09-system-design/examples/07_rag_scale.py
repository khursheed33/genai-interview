"""07_rag_scale.py — flagship planner: vectors, GPUs, cache savings, tenant walls.

Run: uv run python topics/09-system-design/examples/07_rag_scale.py
"""

# --- data plane: docs -> chunks -> vectors + metadata ---
DOCS, CHUNKS_PER_DOC, DIM, BYTES = 1_000_000, 20, 768, 4
vec_gb = DOCS * CHUNKS_PER_DOC * DIM * BYTES / 1e9
meta_gb = DOCS * CHUNKS_PER_DOC * 500 / 1e9  # text + ACL tags + timestamps!
print(f"vectors: {vec_gb:.0f}GB + metadata {meta_gb:.0f}GB (HNSW +50% RAM!)")
assert 50 < vec_gb < 70

# --- serving plane: embed + search + LLM (LLM dominates!) ---
QPS = 100
embed_ms, search_ms, llm_ms = 50, 100, 2000
print(f"per query: embed {embed_ms} + search {search_ms} + LLM {llm_ms}ms (GPUs = budget!)")
gpu_queries_per_s = 1 / (llm_ms / 1000)  # one stream per GPU-ish (illustrative!)
streams = round(QPS / gpu_queries_per_s)
print(f"1 GPU-stream ~ {gpu_queries_per_s:.1f} qps -> {QPS} QPS needs ~{streams}!")

# --- cache levers: exact 30% + semantic 20% = HALF the GPUs! ---
exact_hit, sem_hit = 0.30, 0.20
billed = QPS * (1 - exact_hit - sem_hit)
print(f"cache: {exact_hit:.0%}+{sem_hit:.0%} free -> billed {billed:.0f}/{QPS} QPS!")
assert round(billed) == 50  # float dust: 49.999... (floats lie, round them!)

# --- cost per 1k queries (illustrative $/1M tokens!) ---
TOKENS_PER_Q = 3000  # 2k context + 1k out
cost_1k = TOKENS_PER_Q * 1000 / 1e6 * 2.0  # $2/1M blended
print(f"~${cost_1k:.0f} per 1k queries pre-cache -> ${cost_1k * 0.5:.0f} post-cache")
print("OK — versioned re-index (alias flip!), tenant filter at retrieval, cache halves fleet!")
