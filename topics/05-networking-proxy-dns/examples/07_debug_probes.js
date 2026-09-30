// 07_debug_probes.js — doctor's first three tools, offline-safe (localhost only)
// Run: node topics/05-networking-proxy-dns/examples/07_debug_probes.js
import dns from "node:dns/promises";
import http from "node:http";
import net from "node:net";

// 1. DNS: localhost must resolve (proves resolver path, no internet needed)
const { address } = await dns.lookup("localhost");
console.log("dig localhost ->", address);

// 2. TCP: is the door open? (telnet/nc equivalent)
const srv = http.createServer((_req, res) => res.end('{"ok":true}'));
await new Promise((r) => srv.listen(0, "127.0.0.1", r));
const port = srv.address().port;
const open = await new Promise((resolve) => {
  const s = net.connect(port, "127.0.0.1", () => { s.end(); resolve(true); });
  s.on("error", () => resolve(false));
});
console.log(`nc -vz 127.0.0.1 ${port} ->`, open ? "open" : "closed");

// 3. curl -w timings: split DNS vs connect vs TTFB
const t0 = performance.now();
const res = await fetch(`http://127.0.0.1:${port}/health`);
await res.text();
console.log(`curl total ${(performance.now() - t0).toFixed(1)}ms status=${res.status}`);
srv.close();
console.log("OK — dig→nc→curl-timings: cheap first, always split DNS vs TLS vs app");
