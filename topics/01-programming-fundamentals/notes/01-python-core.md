# 01 — Python Core: Boxes, Lists & Magic Conveyors

Think like a 5-year-old. Python is a toy room. Variables are **labels on boxes**.

## 1. Data types = types of toys

| Type | Toy analogy | Example |
|---|---|---|
| `int`, `float` | Counting blocks | `age = 5`, `price = 9.99` |
| `str` | Name sticker (can't change letters, only make new sticker) | `"asha"` |
| `list` | School bag — you can add/remove tiffin | `[1,2,3]` |
| `tuple` | Sealed birthday gift — can't change | `(1,2)` |
| `dict` | Pencil box with labels: `{"pen": 2}` | fast lookup |
| `set` | Marble bag — no duplicates, no order | `{1,2,2} → {1,2}` |
| `None`, `bool` | Empty plate / light ON-OFF | `None`, `True` |

Real world: Swiggy order = `dict` (`{"id": 101, "items": [...]}`), cart items = `list`, order status = `str`.

## 2. Mutability = can you change the toy itself?

- **Mutable (change inside the bag):** `list, dict, set, bytearray`
- **Immutable (must make a new toy):** `str, int, float, tuple, frozenset`

```python
bag = [1, 2]  # mutable
same_bag = bag
bag.append(3)  # both see [1,2,3] — same bag!

name = "ram"  # immutable
other = name
name = name + "a"  # new sticker, `other` still "ram"
```

Interview trap:

```python
def add(item, box=[]):  # NEVER do this — default list is ONE shared bag!
    box.append(item)
    return box
```

Fix: `def add(item, box=None): box = box or []`.

Real world bug: shared default = one classroom register used by two classes. Attendance mixes up.

## 3. Comprehensions = lunchbox packing in one line

```python
# normal
squares = []
for i in range(5):
    squares.append(i * i)

# same in one line — faster to read once used to it
squares = [i * i for i in range(5)]
evens = {x for x in range(10) if x % 2 == 0}  # set
prices = {"id1": 100, "id2": 200}
gst = {k: v * 1.18 for k, v in prices.items()}  # dict
```

Real world: filter PII emails from user list: `[u for u in users if not u["is_deleted"]]`.

## 4. Iterators vs Generators = book vs live counter

- **Iterable:** the bookshelf (`list`, `str` — has `__iter__`).
- **Iterator:** the finger pointing at next book (`__next__`, raises `StopIteration` at end).
- **Generator:** a factory that makes one toy at a time, sleeps in between (`yield`). Uses almost no memory.

```python
# iterator
it = iter([10, 20])
print(next(it))  # 10


# generator — like a water tap, not a bucket
def numbers(n):
    for i in range(n):
        yield i * i  # pause here, resume on next()


for x in numbers(1_000_000):  # never stores 1M items
    pass
```

Real world: reading a 10 GB log file. `readlines()` = try to lift whole bucket (OOM). `for line in open(...)` = sip with straw (generator). Always stream large files, LLM tokens, CSV rows.

`yield from`, generator expressions: `(x*x for x in range(10))` — parentheses, lazy.

## 5. Quick mental model

- Need to change inside? → mutable (`list/dict/set`).
- Need fixed key? → immutable (`tuple/str`) — can be dict key.
- Building a list to loop once over huge data? → generator.
- Interview one-liners:
  - "Mutable default args share one object — use `None`."
  - "Generators are lazy, O(1) memory — use for streams/files."
  - "`dict/set` lookup is O(1) average — use for dedup/membership."

See runnable code: `../examples/01_mutability.py`, `02_comprehensions_generators.py`.
