# Observability Notes

## Three signals
**Logs** explain events. **Metrics** summarize behavior over time. **Traces** follow one request across components. Correlation IDs connect logs and traces.

## SRE thinking
Define an SLI such as successful requests or latency, then an SLO such as a target percentage over a window. An error budget turns reliability into an explicit engineering constraint. Alerts should be actionable rather than simply noisy.

## Tooling
Structured JSON logs work well for machines. Prometheus stores time-series metrics; Grafana visualizes them. OpenTelemetry provides vendor-neutral telemetry instrumentation. Jaeger and similar systems visualize traces.

## Incident workflow
Detect → triage → mitigate → communicate → recover → investigate root/system causes → document corrective actions. An RCA should explain contributing conditions and prevention, not just identify a person or line of code.

## GenAI observability
Track model, prompt/version, latency, input/output tokens, retrieval quality, tool calls, errors, safety decisions, cost, and user feedback. Avoid storing sensitive prompts without a clear data policy.

## Practice
Create JSON logs with correlation IDs, instrument a request path with metrics/traces, define an SLO and alert, then write an RCA for a simulated outage.