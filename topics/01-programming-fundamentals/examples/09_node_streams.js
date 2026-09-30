// 09_node_streams.js — tap, not bucket (stream  big file without OOM)
// Run: node topics/01-programming-fundamentals/examples/09_node_streams.js
import { Readable, Transform } from "node:stream";
import { Buffer } from "node:buffer";

// Buffer: raw bytes (images, pdf, audio chunks live here, not in strings)
const buf = Buffer.from("dosa");
console.log("buffer:", buf, "len:", buf.length);

// Stream: process 1M rows without storing them
let n = 0;
const source = Readable({
  read() {
    n++;
    if (n > 1_000_000) this.push(null); // end
    else this.push(`row-${n}\n`);
  },
});
const upper = new Transform({
  transform(chunk, _enc, cb) { cb(null, chunk.toString().toUpperCase().slice(0, 20)); },
});
let chunks = 0;
source.pipe(upper).on("data", () => chunks++).on("end", () => {
  console.log("streamed chunks:", chunks > 0 ? "many (lazy)" : "none");
  console.log("OK — pipe() large files/LLM responses, never read all at once");
});
