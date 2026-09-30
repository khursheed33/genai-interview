# Interview Questions — Programming Fundamentals

Answers are one-paragraph + real-world hook. Say the **bold line** first, then the example.

## Python core

- [ ] **[theory]** Mutable vs immutable? Name 3 each + why dict keys must be immutable.
  - **Mutable (`list/dict/set`) change in place; immutable (`str/tuple/int/frozenset`) make new objects. Dict keys must be hashable → immutable.**
  - Example: `bag=[1]; b=bag; bag.append(2)` → both `[1,2]`; `"ram"+"a"` makes new string. Real bug: using `list` as dict key → `TypeError`.
- [ ] **[hands-on]** What's wrong with `def f(x, box=[])`? Fix it.
  - **Default evaluated once — one shared list for all calls. Use `box=None` + create inside.**
  - Real world: two classes sharing one attendance register.
- [ ] **[hands-on]** List vs generator for a 10 GB file? Show both.
  - **`open(...).readlines()` loads all (OOM); `for line in open(...)` streams lazily (O(1) memory). Use `(x for x in ...)` / `yield`.**
- [ ] **[theory]** Iterator vs iterable vs generator?
  - **Iterable has `__iter__`; iterator has `__next__`; generator (`yield`) is a lazy iterator that pauses.**
- [ ] **[hands-on]** Write a decorator `@timer` preserving `__name__`.
  - **Wrapper with `*args/**kwargs` + `@functools.wraps`. Decorator with args = 3 nested levels.**
  - Uses: `@retry`, `@require_auth`, `@cache` in FastAPI.
- [ ] **[hands-on]** Write a context manager for a DB transaction (commit/rollback).
  - **`@contextmanager` + `try: yield; commit / except: rollback; raise`, or class with `__enter__/__exit__`. `with` guarantees cleanup.**

## Python OOP / typing / tooling

- [ ] **[theory]** `@classmethod` vs `@staticmethod` vs `@property`?
  - **classmethod gets `cls` (alternate constructors like `Order.empty()`); staticmethod gets nothing (helper like `gst(x)`); property looks like attribute but runs code.**
- [ ] **[theory]** 3 dunders you must know?
  - **`__init__` (build), `__repr__/__str__` (dev/user view), `__len__/__iter__`, `__enter__/__exit__`, `__call__`.**
- [ ] **[hands-on]** Dataclass vs Pydantic?
  - **Dataclass = boilerplate saver, trusts input. Pydantic = validates/parses at boundary (FastAPI, LangGraph state), `model_dump()`, structured errors.**
- [ ] **[theory]** `asyncio` vs threads vs processes + GIL in one minute?
  - **Async = one cook juggling waits (I/O: APIs/LLM). Threads = many cooks, one burner (GIL) — good for blocking I/O only. Processes = many kitchens — for CPU math. GIL = one thread runs Python bytecode at a time.**
  - Follow-up: blocking `requests.get` inside `async def` freezes the loop — use `httpx.AsyncClient` / `run_in_executor`.
- [ ] **[scenario]** FastAPI endpoint: `def` or `async def`?
  - **`async def` for async I/O (DB/LLM via async client); plain `def` runs in threadpool (fine for sync libs). Never block the loop.**
- [ ] **[theory]** venv/uv, custom exceptions, logging levels?
  - **One venv per project (`uv sync`, commit lock, never `.venv/`). Custom exceptions = specific alarms (`PaymentFailed`) — catch precisely, `raise` don't swallow, `else/finally` for happy-path/cleanup. Logging (`INFO/WARNING/ERROR`) with context (`order_id=`) > print; never log PII.**

## JavaScript / TypeScript / Node

- [ ] **[hands-on]** Closure example + 2 real uses?
  - **Function + its birth variables: `makeCounter()` with private `count`. Uses: `requireAuth(role)` middleware factory, React state, debounce.**
- [ ] **[theory]** What does `this` depend on? Why do arrows differ?
  - **On the caller (`obj.m()` → `obj`), not birthplace. Detached `const g = obj.m; g()` loses it (ESM strict throws). Arrows have no own `this` — inherit parent's. Fix with `.bind`.**
- [ ] **[theory]** `var` vs `let` in a `setTimeout` loop?
  - **`var` is function-scoped + hoisted → prints `3 3 3`; `let` is per-iteration → `0 1 2`.**
- [ ] **[theory]** Microtask vs macrotask order for `Promise.then` vs `setTimeout(0)`?
  - **Microtasks (promises/`process.nextTick`) run before next macrotask (timers/I/O). So `1, bill, water, dosa`.**
- [ ] **[hands-on]** `Promise.all` vs `allSettled` vs `race` vs `any`?
  - **all = parallel, fail-fast (LLM fan-out). allSettled = all results even failures. race = first settled (timeout pattern). any = first success.**
- [ ] **[theory]** CJS vs ESM?
  - **`require/module.exports` (sync, dynamic) vs `import/export` (static, tree-shakeable). New code ESM (`"type": "module"`); mixing breaks `__dirname`.**
- [ ] **[hands-on]** TS: `interface` vs `type`, generics, one utility type?
  - **`interface` = extendable object shape; `type` = unions/aliases (`"new"|"paid"` kills invalid strings). Generic `first<T>(xs: T[])` reuses logic. Utilities: `Pick/Partial/Required/Omit/Record`.**
- [ ] **[theory]** Node: buffers, streams, workers, cluster?
  - **Buffer = raw bytes (files/images). Stream = tap not bucket — `pipe()` GB files without OOM. Worker threads = extra cooks for CPU. Cluster = one process per core sharing a port (PM2).**
- [ ] **[theory]** `package-lock.json`, npm vs pnpm, `^` vs `~`?
  - **Lockfile = exact bill, always commit. pnpm saves disk via symlinks. `^2.3.1` allows minor+patch, `~2.3.1` patch only; MAJOR = breaking.**

## DSA / Big-O / patterns / concurrency

- [ ] **[theory]** Big-O of `dict` lookup, binary search, `sorted()`?
  - **O(1) avg, O(log n), O(n log n). Dropping constants; worst-case counts.**
- [ ] **[hands-on]** Two-sum in O(n)? Longest unique substring?
  - **Two-sum: hashmap of seen values, one pass. Longest-unique: sliding window + last-seen map (see `examples/10`, exercise-05).**
- [ ] **[hands-on]** When heap? Stack vs queue vs tree vs graph one-liner each?
  - **Heap (`heapq.nlargest`) for top-k. Stack LIFO (undo/DFS), queue FIFO (BFS/tasks), tree (files/DOM), graph (friends/knowledge-graph: BFS shortest hops).**
- [ ] **[theory]** SOLID in 60 seconds with one example?
  - **S: `Order`≠`BillPrinter`. O: new payment via Strategy, no edit. L: subclass works as parent. I: split `Flyer/Walker`. D: depend on `Payment` interface, inject it (FastAPI `Depends`).**
- [ ] **[hands-on]** Factory vs Builder vs Adapter vs Strategy vs Observer vs Repository vs DI?
  - **Factory: `make_llm(kind)`. Builder: stepwise thali/pipeline. Adapter: plug converter for legacy API. Strategy: swappable `UPIPay/CardPay`. Observer: subscribe/notify (events). Repository: `OrderRepo.get` hides SQL. DI: pass `llm_client` in, mock in tests.**
- [ ] **[scenario]** Race condition example + fix? Deadlock?
  - **Two threads read 100, both +50, write 150 (lost update) — fix with `Lock`/transaction. Deadlock = A waits B's fork while B waits A's spoon (circular wait) — fix with lock order + timeouts.**
- [ ] **[theory]** Lock vs semaphore vs "thread-safe"?
  - **Lock = bathroom key (1). Semaphore(n) = n seats (cap 10 LLM calls). Thread-safe = correct under concurrency (`queue.Queue`, immutable, locks).**

## Gotchas checklist (say these unprompted for bonus points)

- Mutable defaults share state; `field(default_factory=list)` in dataclasses.
- `await` in `for` loop = serial; wrap with `asyncio.gather` / `Promise.all`.
- ESM `this` loss throws; `.bind` or arrow.
- `list` scan O(n) vs `set` O(1) decides p99 (e.g. visited-URL set in crawler).
- Unbounded caches / global embedding lists leak memory — bound them.

## Self-score (0–5)

- Python core: __ / OOP+typing: __ / async+tooling: __ / JS+TS+Node: __ / DSA: __ / patterns+concurrency: __
- Can I whiteboard: retry decorator / semaphore-limited fan-out / sliding-window / Strategy+DI? Y/N each.
