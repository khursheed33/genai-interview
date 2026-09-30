// 08_http_cache.js — free refills: 200 once, 304 forever (node:http, offline)
// Run: node topics/07-caching/examples/08_http_cache.js
import http from "node:http";
import { createHash } from "node:crypto";

const MENU = JSON.stringify(["dosa", "idli"]);
const etag = `"${createHash("sha256").update(MENU).digest("hex").slice(0, 12)}"`;
const srv = http.createServer((req, res) => {
  if (req.headers["if-none-match"] === etag) { res.writeHead(304).end(); return; } // fingerprint matches!
  res.writeHead(200, { "ETag": etag, "Cache-Control": "max-age=60" }).end(MENU);
});
await new Promise((r) => srv.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${srv.address().port}/menu`;

const first = await fetch(base);
const tag = first.headers.get("etag");
const second = await fetch(base, { headers: { "If-None-Match": tag } });
console.log("first:", first.status, await first.text(), "| second:", second.status, "(empty body, bytes saved!)");
srv.close();
console.log("OK — ETag→304; browsers+CDNs become free Redis (see topic 02 for the full rite)");
