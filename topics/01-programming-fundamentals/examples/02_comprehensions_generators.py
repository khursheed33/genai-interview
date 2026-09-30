"""02_comprehensions_generators.py — lunchbox packing vs factory conveyor.

Run: uv run python topics/01-programming-fundamentals/examples/02_comprehensions_generators.py
"""

import sys

# Comprehension: pack lunchbox in one line
squares = [i * i for i in range(5)]
print("squares:", squares)  # [0,1,4,9,16]

users = [
    {"name": "asha", "deleted": False},
    {"name": "bob", "deleted": True},
]
active = [u["name"] for u in users if not u["deleted"]]
print("active users:", active)  # ['asha']


# Generator: factory makes one toy at a time (tiny memory)
def squares_gen(n):
    for i in range(n):
        yield i * i


big_list = [i * i for i in range(100_000)]
big_gen = (i * i for i in range(100_000))
print("list bytes:", sys.getsizeof(big_list), "| gen bytes:", sys.getsizeof(big_gen))
assert sys.getsizeof(big_gen) < sys.getsizeof(big_list)

# Streaming a big file the right way (lazy, never loads all)
total = 0
for _x in squares_gen(1_000_000):
    total += 0  # pretend work
print("streamed 1M items without storing them. OK")
