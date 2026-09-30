# 06 — LLM Caching: Same Question, Free Answer (semantic + prompt + KV)

LLM calls cost $$$ + seconds. Three caches, three levels:

## 1. Exact & semantic cache (don't CALL for asked questions!)

- **Exact**: `sha256(normalized_prompt + model + temp)` → stored answer (Redis, TTL days). Normalization matters (`"Hi!"` vs `"hi "` = same? strip+lower+sort-context!).
- **Semantic**: NEW question, SAME meaning ("refund policy?" ≈ "how do I get money back?") → embed both, cosine ≥ 0.95 → serve cached. Stack: **GPTCache / Redis semantic** (vector + threshold + verify!). Demo with Jaccard in `../examples/07_semantic_cache.py` (offline twin of embedding similarity!).
- Safety: NEVER cache across users/tenants (leak!) or for fresh/time-sensitive (prices, "today's menu"!) — key includes `tenant + date` where needed. Hit-rate + $saved on dashboard (sells itself!).

## 2. Prompt caching (provider-side: don't RE-SEND the constitution!)

System prompt + RAG context (10k tokens!) resent EVERY turn = billed EVERY turn. **Prompt caching** (Anthropic/OpenAI/ Bedrock): provider caches the PREFIX, you pay ~10% on hits. Rules: stable prefix FIRST (system → context → user last!), 5-min–1h TTL, watch `cache_read` vs `cache_creation` in usage (topic 23 billing!).

## 3. KV cache (inside the GPU: don't RE-THINK tokens!)

Transformer decoding re-reads all previous keys/values per token — **KV cache** stores them (VRAM!). Math: `2 (K+V) × layers × dim × bytes × tokens`. Llama-70B fp16, 4k ctx ≈ 10+ GB JUST for KV! Evict (sliding-window), quantize (int8 KV), page it (**PagedAttention**/vLLM — topic 23!). Long-context bills VRAM, not just time.

One-liner: **"Exact for repeats, semantic (0.95+) for paraphrases, provider prefix-cache for long contexts, KV math before bragging about 128k windows."**
