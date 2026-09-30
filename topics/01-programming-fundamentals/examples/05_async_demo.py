"""05_async_demo.py — one smart cook (asyncio) vs staring at milk (sync).

Run: uv run python topics/01-programming-fundamentals/examples/05_async_demo.py
Expected: sequential ~2s, parallel ~1s.
"""

import asyncio
import time


async def call_llm(name, delay):
    await asyncio.sleep(delay)  # I/O wait — others can work
    return f"{name} done"


async def sequential():
    t0 = time.perf_counter()
    a = await call_llm("a", 1)
    b = await call_llm("b", 1)
    return time.perf_counter() - t0, (a, b)


async def parallel():
    t0 = time.perf_counter()
    res = await asyncio.gather(call_llm("a", 1), call_llm("b", 1))
    return time.perf_counter() - t0, res


async def limited():
    sem = asyncio.Semaphore(2)  # max 2 at once — don't DDoS the provider

    async def guarded(i):
        async with sem:
            return await call_llm(f"q{i}", 0.2)

    return await asyncio.gather(*[guarded(i) for i in range(5)])


async def main():
    t_seq, _ = await sequential()
    t_par, res = await parallel()
    print(f"sequential: {t_seq:.1f}s | parallel: {t_par:.1f}s -> {res}")
    assert t_par < t_seq
    out = await limited()
    print("semaphore batch:", out)


asyncio.run(main())
print("OK — async for waiting (API/DB/LLM), processes for CPU math")
