// 10_fetch_client.js — waiter with badge, token & patience (offline-runnable, mocked fetch)
// Run: node topics/02-api-design-web-protocols/examples/10_fetch_client.js

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Mock server: 1st call 429 + Retry-After, then 200. Counts attempts.
let attempts = 0;
async function mockFetch(_url, opts) {
  attempts++;
  if (attempts === 1)
    return { status: 429, headers: { get: (h) => (h === "Retry-After" ? "1" : null) }, json: async () => ({}) };
  return {
    status: 200,
    headers: { get: () => null },
    json: async () => ({ ok: true, trace: opts.headers["X-Request-ID"] }),
  };
}

async function apiFetch(url, { token, requestId = `req_${Math.random().toString(36).slice(2, 8)}`, tries = 3 } = {}) {
  for (let i = 0; i < tries; i++) {
    const res = await mockFetch(url, {
      headers: { Authorization: `Bearer ${token}`, "X-Request-ID": requestId }, // badge + trace
    });
    if (res.status === 429 || res.status >= 500) {
      const wait = Number(res.headers.get("Retry-After") || 0) * 200 + 2 ** i * 50; // honor server + backoff
      await sleep(wait);
      continue;
    }
    if (res.status === 401) throw new Error("who are you? login (401)");
    return res.json();
  }
  throw new Error("too many retries");
}

const out = await apiFetch("https://api.shop.com/orders/101", { token: "good-token" });
console.log("result:", out, "| attempts:", attempts); // 200 on 2nd try
console.log("OK — badge (auth) + trace ID on every call; honor Retry-After; retry 429/5xx only");
