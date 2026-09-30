// 07_node_http_api.js — street cart API with zero deps (node:http only)
// Run: node topics/03-backend-frameworks/examples/07_node_http_api.js
// Shows Express-style middleware + routing + JSON validation without npm install.
import http from "node:http";

const log = [];
const mws = [
  (req, _res, next) => { req.id = `req_${Math.random().toString(36).slice(2, 8)}`; next(); }, // trace
  (req, res, next) => { // auth before billable work
    if (req.headers.authorization !== "Bearer good") { res.writeHead(401).end('{"title":"login!"}'); return; }
    next();
  },
];
const routes = {
  "GET /orders": (req, res) => res.writeHead(200, { "X-Request-ID": req.id }).end('{"data":[{"id":1}]}'),
};

const srv = http.createServer((req, res) => {
  log.push(`${req.method} ${req.url}`);
  let i = 0;
  const next = () => (i < mws.length ? mws[i++](req, res, next) : routes[`${req.method} ${req.url}`]?.(req, res) ?? res.writeHead(404).end("{}"));
  next();
});
await new Promise((r) => srv.listen(0, r));
const base = `http://127.0.0.1:${srv.address().port}`;

const no = await fetch(`${base}/orders`); // no badge
const ok = await fetch(`${base}/orders`, { headers: { Authorization: "Bearer good" } });
console.log("no-auth:", no.status, "| auth:", ok.status, await ok.text(), "| trace:", ok.headers.get("x-request-id"));
srv.close();
console.log("LOG:", log[0]);
console.log("OK — same onion (trace→auth→route) in every framework's uniform");
