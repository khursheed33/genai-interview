# LLM Serving and LLMOps Notes

## Inference metrics
TTFT is time to first token; TPOT is time per output token. Total latency also includes queueing, prompt processing, generation, network, and post-processing. Capacity planning must consider concurrency and sequence lengths.

## Serving engines
vLLM and TGI focus on efficient serving. llama.cpp targets efficient local inference for supported models. Ollama packages local model workflows. Performance depends on model and hardware.

## Efficiency
Continuous batching improves utilization by scheduling requests dynamically. PagedAttention-style memory management reduces KV-cache fragmentation. Quantization reduces memory and can improve throughput with possible quality loss.

## Operations
A gateway can centralize routing, retries, budgets, provider abstraction, logging, and policy. LLMOps also needs prompt/model versioning, canary releases, evaluation gates, rollback, and cost monitoring.

## Practice
Estimate model memory, benchmark TTFT/TPOT, compare batching strategies, add a gateway, implement a token budget, and create a prompt regression gate.