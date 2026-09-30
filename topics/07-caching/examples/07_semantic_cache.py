"""07_semantic_cache.py — asked? paraphrased? free answer (offline Jaccard twin).

Run: uv run python topics/07-caching/examples/07_semantic_cache.py
Prod uses embeddings + cosine>=0.95; here Jaccard word-overlap teaches the SHAPE.
"""

import hashlib
import re


def normalize(q):
    return re.sub(r"\s+", " ", q.strip().lower().rstrip("?!."))


def exact_key(model, q, temp=0):
    return hashlib.sha256(f"{model}|{temp}|{normalize(q)}".encode()).hexdigest()[:16]


assert exact_key("gpt", "Hi! ") == exact_key("gpt", "hi")
print("exact: 'Hi! ' == 'hi' after normalize (strip+lower+punct)")


def jaccard(a, b):
    sa, sb = set(normalize(a).split()), set(normalize(b).split())
    return len(sa & sb) / len(sa | sb)


CACHE = {"how do i get money back for my order": "Refund in 3-5 days to source."}
THRESH = 0.5  # prod embedding threshold ~0.95; words need a lower bar


def ask(q):
    if normalize(q) in CACHE:
        return CACHE[normalize(q)], "exact"
    best, score = None, 0.0
    for k in CACHE:
        s = jaccard(q, k)
        if s > score:
            best, score = k, s
    if score >= THRESH:
        return CACHE[best], f"semantic({score:.2f})"
    return None, "miss ($$$ LLM call!)"


ans, how = ask("How do I get my money back for the order?!")
assert how.startswith("semantic") and "Refund" in ans
assert ask("dosa price today")[1].startswith("miss")
print("paraphrase ->", how, "| fresh question -> miss (never cache prices!)")

# KV-cache VRAM math: 2(K+V) x layers x dim x bytes x tokens (Llama-70B fp16, 4k ctx)
gb = 2 * 80 * 8192 * 2 * 4096 / 1e9
print(f"KV for 4k ctx ~ {gb:.1f} GB JUST for cache (evict/quantize/page it!)")
print("OK — exact for repeats, semantic for paraphrases, key includes tenant+date!")
