"""Solution: storage math, cache math, fleet math (finance loves all three)."""

import math


def vector_gb(docs, chunks, dim, bytes_=4):
    return docs * chunks * dim * bytes_ / 1e9


def monthly_cost(queries_per_day, tokens_per_q, usd_per_m, cache_hit=0.0):
    billed = queries_per_day * 30 * (1 - cache_hit)
    return billed * tokens_per_q / 1e6 * usd_per_m


def gpus_needed(qps, sec_per_query, per_gpu=1):
    return math.ceil(qps * sec_per_query / per_gpu)
