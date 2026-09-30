// 08_auth_client.js — badge auto-renewal + PKCE challenge (offline, mocked server)
// Run: node topics/04-auth-security/examples/08_auth_client.js
import { createHash, randomBytes } from "node:crypto";

// --- PKCE (S256): verifier hidden, challenge public ---
const verifier = randomBytes(48).toString("base64url");
const challenge = createHash("sha256").update(verifier).digest("base64url");
console.log("verifier len:", verifier.length, "| challenge:", challenge.slice(0, 12) + "...");

// --- fetch wrapper: Bearer + single 401-refresh-and-retry ---
let access = "expired-token";
async function mockFetch(url, opts = {}) {
  if (url.endsWith("/refresh")) return { status: 200, json: async () => ({ access: "fresh-token" }) };
  const token = (opts.headers?.Authorization ?? "").split(" ")[1];
  if (token === "expired-token") return { status: 401, json: async () => ({}) };
  return { status: 200, json: async () => ({ data: "secret-menu" }) };
}
async function api(url, retried = false) {
  const res = await mockFetch(url, { headers: { Authorization: `Bearer ${access}` } });
  if (res.status === 401 && !retried) { // exactly ONE renewal, then retry
    access = (await (await mockFetch("https://api/refresh", {})).json()).access;
    return api(url, true);
  }
  if (res.status === 401) throw new Error("session dead — send user to login");
  return res.json();
}
console.log("result:", await api("https://api/orders"), "| token now:", access);
console.log("OK — attach Bearer, refresh once on 401, then login; PKCE challenge = sha256(verifier)");
