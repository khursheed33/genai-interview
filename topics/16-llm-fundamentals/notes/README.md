# LLM Fundamentals Notes

## Transformer mental model
A transformer processes token representations using attention. Self-attention lets each token weigh other tokens; multi-head attention captures different relationships. Feed-forward layers transform representations, while residual connections and normalization stabilize deep networks.

## Model families
BERT is primarily encoder-oriented and strong for representation/classification tasks. GPT-style models are decoder-oriented and designed for autoregressive generation. T5 uses an encoder-decoder formulation and frames tasks as text-to-text.

## Training
Pretraining learns statistical patterns from large corpora. Instruction tuning improves task following. RLHF uses preference feedback with reinforcement learning; DPO directly optimizes preference pairs without the same online RL loop.

## Tokens and context
Tokenization converts text into model units. Context windows limit how much information a request can contain. Longer context does not automatically mean better reasoning; irrelevant or conflicting context can still reduce quality.

## Sampling
Temperature changes randomness; top-p limits the probability mass considered. Greedy decoding chooses the highest-probability next token. Structured output/function calling constrains the interface between a model and software.

## Hallucination and deployment
Hallucination is generation that is unsupported or incorrect. Grounding, retrieval, constrained outputs, verification, and evaluation reduce risk but do not make models infallible. Quantization reduces memory/compute at a possible quality cost.

## Practice
Explain attention with a toy example, compare BERT/GPT/T5, inspect tokenization, experiment with sampling, design a JSON tool call, and measure how context changes an answer.