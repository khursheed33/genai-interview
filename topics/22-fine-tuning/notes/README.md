# Fine-Tuning Notes

## When to fine-tune
Fine-tuning is useful for consistent behavior, style, formatting, domain task patterns, or specialized instruction following. Do not use it as the default mechanism for rapidly changing factual knowledge that can be retrieved.

## Methods
SFT trains on curated demonstrations. Preference methods such as DPO learn from preferred/rejected outputs. RLHF adds a preference model and reinforcement-learning stage. PEFT methods update a small parameter subset. LoRA learns low-rank adapters; QLoRA combines quantized base weights with adapter training.

## Data quality
Training data should be representative, deduplicated, correctly formatted, permissioned, and split into train/validation/test sets. Poor examples teach poor behavior. Remove secrets and unnecessary personal data.

## Failure modes
Overfitting can improve training metrics while hurting generalization. Catastrophic forgetting can degrade capabilities. Data leakage makes evaluation misleading. Checkpoint merging and distillation introduce their own quality trade-offs.

## Infrastructure
Hugging Face Transformers, TRL, Accelerate, DeepSpeed, and FSDP address different pieces of training and distributed execution. Plan GPU memory, sequence length, batch size, gradient accumulation, checkpointing, and reproducibility.

## Practice
Prepare a small instruction dataset, build a validation split, compare baseline vs SFT, experiment with LoRA/QLoRA, inspect failure cases, and document whether the improvement justifies training cost.