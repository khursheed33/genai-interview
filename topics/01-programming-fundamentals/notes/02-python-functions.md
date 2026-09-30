# 02 — Python Functions: Gift Wrap (Decorators) & Library Books (Context Managers)

## 1. Decorators = gift wrapping a function

A decorator takes your function (gift), wraps it with extra paper (logging, retry, auth), returns wrapped gift. You still call it the same way.

```python
import time, functools


def timer(func):
    @functools.wraps(func)  # keeps name/docstring — always use it!
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - t0:.3f}s")
        return result

    return wrapper


@timer
def fetch_order(order_id):
    time.sleep(0.1)
    return {"id": order_id}
```

Real world: `@require_auth`, `@retry(3)`, `@cache`, `@rate_limit` in FastAPI/Flask. Order matters — bottom decorator runs first:

```python
@auth  # 2nd
@retry(3)  # 1st
def pay(): ...
```

Interview: `*args/**kwargs` = "any-shaped parcel". `functools.wraps` preserves `__name__`. Decorator with args = 3 nested functions (factory → decorator → wrapper).

## 2. Context managers = borrow library book, auto-return

`with` guarantees cleanup even if you cry (exception) in the middle.

```python
with open("bill.txt") as f:  # auto-closes, even on error
    data = f.read()

import threading

lock = threading.Lock()
with lock:  # auto-releases
    balance += 100
```

Make your own two ways:

```python
# A) class — like a lunchbox with open/close lids
class Timer:
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        print(f"took {time.perf_counter() - self.t0:.3f}s")
        return False  # False = don't hide exceptions


# B) generator — shorter
from contextlib import contextmanager


@contextmanager
def db_transaction(conn):
    try:
        yield conn
        conn.commit()  # happy path
    except Exception:
        conn.rollback()  # sad path
        raise
```

Real world: DB transactions, `Decimal` precision, `torch.no_grad()`, temp dirs, LLM tracing spans.

## 3. Recap (5 bullets)

- Decorator = function that wraps a function (`@` is sugar for `f = deco(f)`).
- Always `*args/**kwargs` + `functools.wraps`.
- `with` = guaranteed setup/teardown; use for files, locks, connections.
- `__enter__/__exit__` or `@contextmanager` + `yield`.
- `__exit__` returning `True` swallows exceptions (rarely want that).

One-liners: "Decorators add cross-cutting concerns without touching logic." / "`with` prevents leaks — file/descriptor/connection."
