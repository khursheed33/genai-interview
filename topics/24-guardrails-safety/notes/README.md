# Guardrails, Safety and Responsible AI Notes

## Defense in depth
Safety should exist at input, orchestration, tool, retrieval, model-output, and post-processing layers. No single prompt instruction is a complete security boundary.

## Threats
Prompt injection attempts to manipulate instructions. Data exfiltration can occur when sensitive context reaches a model or tool. Excessive agency occurs when a model has more permissions than required. Other risks include insecure output handling, supply-chain issues, and sensitive-data leakage.

## Guardrails
Use schema validation, allowlisted tools, authorization checks, content policies, PII detection/redaction, grounding/citations, rate limits, and human approval for high-impact side effects. Tools must enforce authorization independently of the model.

## Evaluation and red teaming
Create adversarial cases for injection, jailbreaks, privacy, unsafe content, tool abuse, and retrieval poisoning. Measure both false positives and false negatives because an over-blocking system can also be unusable.

## Privacy and regulation
Data minimization, purpose limitation, retention, access control, and auditability are foundational privacy practices. Map applicable legal obligations to the actual product, users, jurisdictions, and risk classification rather than assuming one framework applies universally.

## Practice
Implement input PII redaction, output schema validation, tool allowlisting, injection test cases, audit logs, and a human-approval path for irreversible actions.