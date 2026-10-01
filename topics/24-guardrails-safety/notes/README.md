# Guardrails, Safety and Responsible AI Notes

## Defense in depth
Safety belongs at input, orchestration, tool, retrieval, model-output, and post-processing layers. No single prompt instruction is a complete security boundary.

## Threats
Prompt injection manipulates instructions. Data exfiltration exposes sensitive context. Excessive agency gives a model more permissions than needed. Also consider insecure output handling, supply-chain risks, and retrieval poisoning.

## Guardrails
Use schema validation, tool allowlists, authorization checks, content policies, PII detection/redaction, grounding, rate limits, and human approval for high-impact side effects. Tools must enforce authorization independently.

## Evaluation
Red-team injection, jailbreak, privacy, unsafe-content, tool-abuse, and poisoning cases. Measure both false positives and false negatives.

## Practice
Implement PII redaction, output validation, tool allowlisting, injection tests, audit logs, and human approval for irreversible actions.