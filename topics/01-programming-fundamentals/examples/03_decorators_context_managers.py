"""03_decorators_context_managers.py — gift wrap + library book.

Run: uv run python topics/01-programming-fundamentals/examples/03_decorators_context_managers.py
"""

import functools
import time
from contextlib import contextmanager


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - t0:.3f}s")
        return result

    return wrapper


@timer
def fetch_order(order_id):
    time.sleep(0.05)
    return {"id": order_id}


print(fetch_order(101))
assert fetch_order.__name__ == "fetch_order"  # functools.wraps kept the name


# Context manager: borrow book, auto-return even on error
@contextmanager
def fake_db():
    print("open connection")
    conn = {"committed": False}
    try:
        yield conn
        conn["committed"] = True
        print("commit")
    except Exception:
        print("rollback")
        raise


with fake_db() as conn:
    print("...working...", conn)
print("OK — with-block always cleans up")
