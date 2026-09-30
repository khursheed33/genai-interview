// 11_sse_parser.js — reading the ticker tape (LLM token stream parser)
// Run: node topics/02-api-design-web-protocols/examples/11_sse_parser.js

// Parses text/event-stream: "data: X\n\n" blocks, skips comments (:...), stops at [DONE]
function parseSSE(text) {
  const events = [];
  for (const block of text.split("\n\n")) {
    if (!block.trim()) continue;
    // comments are per-LINE (:...), not per-block — drop only those lines!
    const data = block.split("\n").filter((l) => l.startsWith("data: ")).map((l) => l.slice(6));
    if (data.length === 0) continue;
    const joined = data.join("\n");
    if (joined === "[DONE]") break;
    events.push(joined);
  }
  return events;
}

const stream = `: connected (comment, ignored)\ndata: {"token":"Namaste"}\n\ndata: {"token":" dosa"}\n\ndata: [DONE]\n\n`;
const tokens = parseSSE(stream).map((j) => JSON.parse(j).token);
console.log("tokens:", tokens); // ['Namaste', ' dosa']
console.log("sentence:", tokens.join(""));
console.log("OK — SSE: data: lines, blank-line frames, [DONE] terminator, auto-reconnect via Last-Event-ID");
