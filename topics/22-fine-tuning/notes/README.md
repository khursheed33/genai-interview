# Fine-Tuning Notes

## When to fine-tune
Fine-tuning is useful for consistent behavior, style, formatting, or specialized task patterns. It should not be the default solution for rapidly changing factual knowledge.

## Methods
SFT trains on demonstrations. DPO learns from preferred/rejected outputs. RLHF adds preference modeling and reinforcement learning. PEFT updates a small parameter subset. LoRA learns low-rank adapters; QLoRA combines quantized base weights with adapter training.

## Data
Training data should be representative, deduplicated, correctly formatted, permissioned, and split into train/validation/test sets. Remove secrets and unnecessary personal data.

## Failure modes
Watch for overfitting, catastrophic forgetting, leakage, and misleading evaluation. Checkpoint merging and distillation also introduce quality trade-offs.

## Practice
Prepare an instruction dataset, build a validation split, compare baseline vs SFT, experiment with LoRA/QLoRA, inspect failures, and document whether improvement justifies training cost.