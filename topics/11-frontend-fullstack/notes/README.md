# Frontend and Full-Stack Notes

## Browser and accessibility
HTML provides structure, CSS presentation, and JavaScript behavior. Semantic HTML, keyboard navigation, labels, focus management, contrast, and useful error states are part of correctness.

## React
React renders from props and state. Effects synchronize with external systems; avoid using effects for values that can be derived during render. Keep state close to its owner and distinguish server state from UI state.

## Rendering
SSR renders on request, SSG generates ahead of time, ISR regenerates generated content, and Server Components execute on the server to reduce client JavaScript. Choose using freshness, SEO, personalization, and latency.

## LLM streaming
SSE is simple for server-to-client streaming; WebSockets support bidirectional communication. Handle partial output, reconnects, cancellation, backpressure, and errors. A chat generation can be modeled as idle → submitting → streaming → completed/error/cancelled.

## Practice
Build an accessible form, implement a React data-loading state machine, create an SSE chat mock, compare server/client rendering, and profile a slow component.