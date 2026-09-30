"""12_race_lock.py — two kids, one chocolate (race) + bathroom key (lock).

Run: uv run python topics/01-programming-fundamentals/examples/12_race_lock.py
"""

import threading

balance = 0
lock = threading.Lock()


def add_no_lock():
    global balance
    for _ in range(20_000):
        balance += 1  # read-add-write: two cooks overwrite each other


def add_with_lock():
    global balance
    for _ in range(20_000):
        with lock:
            balance += 1


# demo race (may or may not fail on your machine — timing dependent!)
threads = [threading.Thread(target=add_no_lock) for _ in range(4)]
[t.start() for t in threads]
[t.join() for t in threads]
print(f"no-lock balance (expect 80000, often less): {balance}")

balance = 0
threads = [threading.Thread(target=add_with_lock) for _ in range(4)]
[t.start() for t in threads]
[t.join() for t in threads]
print(f"with-lock balance: {balance}")
assert balance == 80000
print("OK — race = lost update; lock = one at a time")
