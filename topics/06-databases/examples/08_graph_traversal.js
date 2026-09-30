// 08_graph_traversal.js — family-tree questions: recommendations + fraud rings
// Run: node topics/06-databases/examples/08_graph_traversal.js
// Same traversals as Cypher MATCH (u:User)-[:BOUGHT]->(i)<-[:BOUGHT]-(s)-[:BOUGHT]->(rec)
const bought = { asha: ["dosa-mix"], bob: ["dosa-mix", "filter-coffee"], cara: ["filter-coffee", "ghee"] };
const friends = { asha: ["bob"], bob: ["asha", "cara"], cara: ["bob"] };

function recommend(user) { // collaborative: strangers who bought what you bought, bought what?
  const mine = new Set(bought[user] ?? []), recs = new Map();
  for (const [other, items] of Object.entries(bought)) {
    if (other === user || !items.some((i) => mine.has(i))) continue;
    for (const i of items) if (!mine.has(i)) recs.set(i, (recs.get(i) ?? 0) + 1);
  }
  return [...recs.entries()].sort((a, b) => b[1] - a[1]).map(([i]) => i);
}
console.log("for asha:", recommend("asha")); // filter-coffee (via bob)

// fraud ring: two "strangers" sharing device/IP/phone?
const usesDevice = { asha: ["d1"], bob: ["d1"], cara: ["d9"] };
function sharedDevice(a, b) { return (usesDevice[a] ?? []).some((d) => (usesDevice[b] ?? []).includes(d)); }
console.log("asha~bob share device?", sharedDevice("asha", "bob")); // true -> review!

// BFS friend-of-friend (2-hop reach, like variable-length Cypher -[*1..2]-)
function fof(user) {
  const seen = new Set([user]), out = new Set();
  for (const f of friends[user] ?? []) for (const g of friends[f] ?? []) {
    if (!seen.has(g) && g !== user) out.add(g);
  }
  return [...out];
}
console.log("fof(asha):", fof("asha")); // cara
console.log("OK — recommendations = 2-hop item paths; fraud = shared-identifier paths; Cypher in notes/06");
