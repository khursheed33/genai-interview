"""Solution: decorator factory (3 levels: factory -> decorator -> wrapper)."""

import functools


def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last = e
            raise last

        return wrapper

    return decorator
