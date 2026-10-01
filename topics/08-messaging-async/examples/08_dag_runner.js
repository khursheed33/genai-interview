// 08_dag_runner.js — conductor: topo order + retries + timing (Airflow/Temporal mini-me)
// Run: node topics/08-messaging-async/examples/08_dag_runner.js
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// DAG: parse -> chunk/embed (parallel) -> upsert; flaky chunk succeeds on retry
const attempts = {};
const tasks = {
  parse: { deps: [], run: async () => "3 pages" },
  chunk: {
    deps: ["parse"],
    run: async () => {
      attempts.chunk = (attempts.chunk ?? 0) + 1;
      if (attempts.chunk < 2) throw new Error("pdf hiccup");
      return "12 chunks";
    },
    retries: 3,
  },
  embed: { deps: ["parse"], run: async () => "12 vectors" },
  upsert: { deps: ["chunk", "embed"], run: async () => "indexed" },
};

async function runDag(tasks) {
  const done = {}, order = [];
  while (Object.keys(done).length < Object.keys(tasks).length) {
    let progress = false;
    for (const [name, t] of Object.entries(tasks)) {
      if (done[name] || !t.deps.every((d) => done[d])) continue;
      let last;
      for (let i = 0; i <= (t.retries ?? 0); i++) {
        try { done[name] = await t.run(); order.push(`${name}(try${i + 1})`); progress = true; break; }
        catch (e) { last = e; await sleep(5); }
      }
      if (!done[name]) throw last;
    }
    if (!progress) throw new Error("cycle or missing dep!");
  }
  return order;
}

const order = await runDag(tasks);
console.log("order:", order.join(" -> "));
console.log("OK — topo order, chunk retried (try2), upsert waited for both (idempotent tasks assumed!)");
