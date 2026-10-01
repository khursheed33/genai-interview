# Agents and Orchestration Notes

## Workflow vs agent
A workflow has a mostly known sequence. An agent chooses actions dynamically using a model and tools. Prefer deterministic workflows when the process is predictable; agents add flexibility but also cost, latency, nondeterminism, and failure modes.

## Tools
Tools need narrow typed contracts, explicit permissions, validation, timeouts, and observable results. The model proposes an action; application code remains responsible for authorization and execution.

## Patterns
ReAct interleaves model decisions with observations. Plan-and-execute separates planning from execution. Single-agent systems are simpler; multi-agent systems need a real reason such as decomposition or parallel ownership.

## Memory
Short-term memory is task state. Long-term memory persists selected facts and requires relevance, privacy, retention, conflict resolution, and deletion policies.

## Reliability
Bound loops, tool permissions, budgets, and timeouts. Make side effects idempotent and audit every action. Never treat model output as authorization.

## Practice
Build a deterministic tool workflow, then an agent version. Add a tool allowlist, loop budget, timeout, audit log, and idempotency key. Compare reliability and cost.