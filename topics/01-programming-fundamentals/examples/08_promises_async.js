// 08_promises_async.js — waiter + token system
// Run: node topics/01-programming-fundamentals/examples/08_promises_async.js

const callLLM = (name, ms) =>
  new Promise((res) => setTimeout(() => res(`${name} done`), ms));

async function main() {
  // microtask (promise) beats macrotask (timeout)
  console.log("1-take order");
  setTimeout(() => console.log("4-serve dosa"), 0);
  Promise.resolve().then(() => console.log("3-give water"));
  console.log("2-write bill");

  // parallel: total = slowest, not sum
  const t0 = Date.now();
  const [a, b] = await Promise.all([callLLM("a", 500), callLLM("b", 500)]);
  console.log(a, b, `parallel took ~${Date.now() - t0}ms`);

  // timeout pattern with race
  const res = await Promise.race([
    callLLM("slow", 2000),
    new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), 300),
  )]).catch((e) => e.message);
  console.log("race result:", res); // timeout

  // allSettled: need every result even if some fail
  const all = await Promise.allSettled([
    Promise.resolve(1), Promise.reject(new Error("bad")),
  ]);
  console.log("settled:", all.map((x) => x.status)); // fulfilled, rejected
}
main().then(() => console.log("OK — Promise.all for parallel I/O"));
