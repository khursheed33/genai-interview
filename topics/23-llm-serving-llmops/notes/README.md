# LLM Serving and LLMOps Notes

## Inference metrics
**TTFT** is time to first token; **TPOT** is time per output token. Total latency depends on queueing, prompt processing, generation, network, and post-processing. Capacity planning must consider concurrency and sequence lengths.

## Serving engines
vLLM and TGI focus on efficient model serving. llama.cpp targets efficient local/CPU-oriented inference for supported models. Ollama packages local model workflows for developer use. Features and performance vary by model/hardware.

## Efficiency
Continuous batching increases utilization by scheduling requests dynamically. PagedAttention-style memory management reduces KV-cache fragmentation. Quantization reduces memory and can improve throughput, with possible quality loss.

## VRAM and cost
Estimate weights, KV cache, activations/overhead, concurrency, and framework overhead. Do not size GPUs using parameter count alone.

## Gateways and operations
A gateway such as LiteLLM or Portkey can centralize routing, retries, budgets, provider abstraction, logging, and policy. Production LLMOps also needs prompt/model versioning, canary releases, evaluation gates, rollback, and cost monitoring.

## Practice
Estimate memory for a model, benchmark TTFT/TPOT, compare batching strategies, add a model gateway, implement a token budget, and create a prompt regression gate in CI.