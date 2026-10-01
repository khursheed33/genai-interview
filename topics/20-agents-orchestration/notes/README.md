# Agents and Orchestration Notes

## Workflow vs agent
A workflow has a mostly known sequence of steps. An agent chooses actions dynamically using a model and tools. Prefer a deterministic workflow when the process is predictable; agents add flexibility but also cost, latency, nondeterminism, and failure modes.

## Tool calling
A tool should have a narrow, typed contract, explicit permissions, validation, timeout, and observable result. The model proposes an action; application code remains responsible for authorization and execution.

## Patterns
ReAct interleaves model decisions with tool observations. Plan-and-execute separates planning from execution. Single-agent systems are simpler; multi-agent systems are useful only when decomposition, ownership, or parallelism genuinely justify coordination.

## Memory
Short-term memory is conversation/task state. Long-term memory persists selected facts or experiences. Memory needs retention, privacy, relevance, conflict resolution, and deletion policies.

## Orchestration
LangGraph, LangChain, LlamaIndex, CrewAI, and AutoGen provide different abstractions for workflows and agents. MCP standardizes how applications expose tools/resources to models. A2A-style protocols address agent-to-agent interaction.

## Safety and reliability
Bound tool permissions, cap loops, set timeouts/budgets, validate outputs, make side effects idempotent, and log every action. Never treat model output as authorization.

## Practice
Build a deterministic tool workflow, then an agent version. Add a tool allowlist, loop budget, timeout, audit log, and idempotency key. Compare reliability and cost.