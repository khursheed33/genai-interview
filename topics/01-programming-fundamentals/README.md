# 01 - Programming Fundamentals

> Scope: README.md section 1: Python, JavaScript/TypeScript/Node.js, Core CS (DSA, Big-O, SOLID, Design Patterns, Concurrency)
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — start with notes in order)
- Python core → `notes/01-python-core.md` (mutability, comprehensions, generators)
- Functions → `notes/02-python-functions.md` (decorators, context managers)
- OOP+typing → `notes/03-python-oop-typing.md` (dunder, dataclass, Pydantic)
- Async+tooling → `notes/04-python-async-tooling.md` (asyncio, GIL, venv, logging, memory)
- JS → `notes/05-javascript.md` (closures, `this`, hoisting, event loop, promises)
- TS+Node → `notes/06-typescript-node.md` (modules, generics, streams/buffers, semver)
- DSA → `notes/07-dsa-big-o.md` (Big-O, two pointers, sliding window, heap)
- Design → `notes/08-solid-patterns-concurrency.md` (SOLID, 9 patterns, race/deadlock)

## Examples (all runnable — verified)
| File | Covers | Run |
|---|---|---|
| `examples/01_mutability.py` | mutable trap + fix | `uv run python topics/01-programming-fundamentals/examples/01_mutability.py` |
| `examples/02_comprehensions_generators.py` | comprehensions, lazy streams | same pattern |
| `examples/03_decorators_context_managers.py` | `@timer`, `fake_db` transaction | same pattern |
| `examples/04_oop_dataclass_pydantic.py` | dunder, dataclass, Pydantic | same pattern |
| `examples/05_async_demo.py` | `gather`, `Semaphore` (~2s→~1s) | same pattern |
| `examples/06_exceptions_logging.py` | custom exc, logging with context | same pattern |
| `examples/07_closures_this.js` | closures, `this`/bind | `node .../07_closures_this.js` |
| `examples/08_promises_async.js` | `all/allSettled/race`, microtasks | `node .../08_promises_async.js` |
| `examples/09_node_streams.js` | Buffer + 1M-row pipe | `node .../09_node_streams.js` |
| `examples/10_dsa_patterns.py` | palindrome, sliding window, top-k | `uv run python ...` |
| `examples/11_patterns_solid.py` | Strategy/Factory/Observer/DI | `uv run python ...` |
| `examples/12_race_lock.py` | race vs Lock | `uv run python ...` |
| `examples/13_typescript_demo.ts` | interfaces, generics, utilities | `node .../13_typescript_demo.ts` |

## Exercises (5 — `uv run pytest topics/01-programming-fundamentals/exercises -q`, 12 tests)
- `exercise-01-mutable-default` — fix shared-list trap
- `exercise-02-generator` — lazy log stream + filter
- `exercise-03-retry-decorator` — `@retry(times=3)` with `functools.wraps`
- `exercise-04-async-parallel` — `gather` + semaphore cap
- `exercise-05-dsa-patterns` — two-sum / sliding window / top-k

## Structure
- `README.md` - this checklist entry point
- `notes/` - your condensed notes (add `.md` per sub-topic)
- `examples/` - runnable minimal examples (python/js/sh)
- `exercises/` - practice tasks + solutions
- `interview-questions.md` - Q and A bank

## How to use
1. Read the checklist item in root README.
2. Add notes + code + diagrams here.
3. Do 2-3 exercises and 1 mini-project link in `projects/` if applicable.
4. Self-quiz with interview questions.

## Resources
- Add links as you learn (docs, papers, videos).
- Prefer primary sources: official docs, RFCs, papers.

## Progress
- [x] Notes drafted (8 files, kid-style + real-world)
- [x] Examples run (13 files, verified: python + node)
- [x] Exercises done (5 exercises, 12 pytest tests green)
- [x] Interview Qs revised (25+ Q/A in `interview-questions.md`)
