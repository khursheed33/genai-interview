# 06 — TypeScript + Node.js Internals + npm

## 1. Modules: CJS vs ESM = two tiffin systems

```js
// CommonJS (old Node): require/module.exports — sync, dynamic
const fs = require("fs"); module.exports = { a: 1 };
// ESM (modern, browsers+Node): import/export — static, tree-shakeable
import fs from "fs"; export const a = 1;
```

Mixing breaks (`__dirname` missing in ESM, need `import.meta.url`). New code: ESM (`"type": "module"` in package.json).

## 2. TypeScript = helmets for JS (labels + guards)

```ts
interface Order { id: number; items: string[]; email?: string } // shape, extendable
type Status = "new" | "paid" | "shipped";                       // union — no invalid string!

function first<T>(xs: T[]): T | undefined { return xs[0]; }     // generic = any-type tiffin
const o = first<Order>(orders);

type PaidOrder = Required<Order>;                 // utility types:
type Preview = Pick<Order, "id" | "items">;       // Pick/Partial/Required/Record/Omit/ReturnType
function pay(o: Order): asserts o is PaidOrder { if (!o.email) throw new Error(); }
```

Real world: `OrderIn` validated by Pydantic (backend) mirrors `interface Order` (frontend) — contract prevents "email missing" prod bug. `strict: true` in tsconfig catches `undefined` early.

## 3. Node internals = single waiter + kitchen helpers

Event loop phases (in order): **timers → pending → poll (I/O) → check (`setImmediate`) → close**. `process.nextTick` + promise microtasks run *between* phases (can starve loop if abused).

- **Buffers:** raw bytes outside V8 heap (`Buffer.from("hi")`) — for files, images, audio chunks. Real world: streaming PDF upload.
- **Streams:** tap, not bucket. `fs.createReadStream().pipe(res)` — 5 GB video without OOM. Types: Readable/Writable/Duplex/Transform. Always `.pipe()` large LLM/file responses.
- **Worker threads:** extra cooks for CPU (share memory via `SharedArrayBuffer`). Unlike browser, Node *can* thread, but still prefer separate service for heavy ML.
- **Clustering:** one waiter per CPU core (`os.cpus()`), all share port via master. PM2 does this. For GenAI: put LLM behind queue + autoscale, not cluster alone.

## 4. npm / semver = kitchen inventory register

`package.json`: name, version, scripts, deps vs devDeps. Lockfile (`package-lock.json`) = exact bill — always commit.

- `npm` (default), `yarn` (fast, workspaces), `pnpm` (disk-saving symlinks, strict). Pick one per repo.
- **Semver** `MAJOR.MINOR.PATCH` (`2.3.1`): MAJOR=breaking (new thali shape), MINOR=feature (extra sweet, safe), PATCH=fix (less salt). `^2.3.1` = allow minor+patch, `~2.3.1` = patch only.

**Recap:** ESM for new code; TS interfaces + unions prevent invalid states; streams/buffers for big data; cluster for CPU cores; lockfile always.
