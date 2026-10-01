// 08_llm_gateway.js — one door, many brains: route, cache, fall back, bill (mocked)
// Run: node topics/09-system-design/examples/08_llm_gateway.js
const cache = new Map(); // exact semantic-lite: normalized prompt -> answer
const usage = {}; // tenant -> {tokens, $}

// mocked providers: [name, $/1M, latencyMs, fails?]
const providers = [
  { name: "haiku", cost: 0.5, ms: 400, fail: false },
  { name: "sonnet", cost: 3, ms: 1200, fail: true }, // outage!
  { name: "opus", cost: 15, ms: 2500, fail: false },
];
function classify(q) { return q.length < 40 ? "easy" : "hard"; } // router: tiny heuristic!

async function call(p, q) {
  await new Promise((r) => setTimeout(r, 10));
  if (p.fail) throw new Error(`${p.name} 503`);
  return `[${p.name}] ${q.slice(0, 20)}...`;
}
async function gateway(tenant, q) {
  const key = `${tenant}|${q.trim().toLowerCase()}`;
  if (cache.has(key)) return { ans: cache.get(key), via: "cache ($0!)" };
  const tier = classify(q) === "easy" ? providers.slice(0, 2) : providers.slice(1);
  let last;
  for (const p of tier) { // cheapest-first with quality floor + fallback!
    try {
      const ans = await call(p, q);
      cache.set(key, ans);
      usage[tenant] = usage[tenant] ?? { calls: 0 };
      usage[tenant].calls++;
      return { ans, via: p.name };
    } catch (e) { last = e; }
  }
  throw last;
}

console.log(await gateway("acme", "hi")); // easy -> haiku
console.log(await gateway("acme", "hi")); // cache!
console.log(await gateway("acme", "Explain Raft log replication in depth please")); // hard -> sonnet fails -> opus!
console.log("usage:", usage);
console.log("OK — route by difficulty, cheapest-first, fallback on 503, cache repeats, bill per tenant!");
