"""Solution: gather for parallel, semaphore to cap concurrency."""

import asyncio


async def fake_call(name, delay=0.2):
    await asyncio.sleep(delay)
    return f"{name} done"


async def run_all(names, delay=0.2):
    return list(await asyncio.gather(*[fake_call(n, delay) for n in names]))


async def run_limited(names, limit=2, delay=0.2):
    sem = asyncio.Semaphore(limit)

    async def guarded(n):
        async with sem:
            return await fake_call(n, delay)

    return list(await asyncio.gather(*[guarded(n) for n in names]))
