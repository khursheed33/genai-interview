# 03 — Python OOP, Dunder, Dataclasses, Pydantic, Typing

Think: **class = biscuit mould, object = biscuit**.

## 1. OOP in one Tiffin box

```python
class Order:
    def __init__(self, items):
        self.items = items  # constructor

    def total(self):
        return sum(self.items)  # method

    @classmethod
    def empty(cls):
        return cls([])  # makes from class, not instance

    @staticmethod
    def gst(x):
        return round(x * 0.18, 2)  # plain helper, no self/cls

    @property
    def count(self):
        return len(self.items)  # use as o.count, not o.count()
```

- **Encapsulation:** hide kitchen (`_private` by convention, `__mangled` for name-mangling).
- **Inheritance:** child reuses parent (`class RefundOrder(Order)`). Prefer **composition** ("has-a") over inheritance ("is-a") for GenAI code — e.g. `Agent` *has* `LLMClient`, not *is* LLM.
- **Polymorphism:** same `pay()` button, UPI/card behave differently (duck typing: "if it quacks, treat as duck").
- **MRO:** Python order for multiple inheritance — `ClassName.__mro__`. Rarely need MI; use mixins/protocols.

## 2. Dunder (double-underscore) = magic buttons

```python
class Cart:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)  # len(cart)

    def __getitem__(self, i):
        return self.items[i]  # cart[0], for x in cart

    def __repr__(self):
        return f"Cart({self.items!r})"  # dev view

    def __str__(self):
        return f"Cart with {len(self)} items"  # user view

    def __eq__(self, o):
        return self.items == o.items
```

Must-know: `__init__`, `__repr__/__str__`, `__len__`, `__iter__/__next__`, `__enter__/__exit__`, `__call__` (make object callable — how frameworks make `model(x)` work).

## 3. Dataclasses = pre-printed form (less writing)

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)  # frozen = immutable, hashable — good for cache keys
class User:
    id: int
    name: str
    tags: list[str] = field(default_factory=list)  # NEVER [] directly!
```

Gets `__init__/__repr__/__eq__` free. Use for DTOs, configs, events.

## 4. Pydantic = strict school guard at gate

Dataclass trusts you; Pydantic **validates** (types, emails, ranges) and parses JSON. Standard in FastAPI + LangChain/LangGraph state.

```python
from pydantic import BaseModel, Field, ValidationError


class OrderIn(BaseModel):
    id: int = Field(gt=0)
    email: str
    items: list[str] = Field(min_length=1)


try:
    OrderIn(id=-1, email="x", items=[])
except ValidationError as e:
    print(e.json())  # structured errors for API response
```

Pydantic v2 is Rust-backed (fast). Use `model_dump()` / `model_validate()`.

## 5. Typing = labels on tiffins so nobody mixes sweets and sambar

```python
from typing import Optional


def total(items: list[int]) -> int: ...


user: dict[str, int] = {}


def fetch(id: int | None = None) -> Optional[dict]: ...  # X | Y needs py3.10+
```

Generics/Protocols: `def first[T](xs: list[T]) -> T` (py3.12 syntax) or `TypeVar`. `Protocol` = "must have these methods" without inheritance.

Check with `mypy`. It catches: `total(["a"])` before production.

**Recap:** class=mould; dunder=magic buttons; dataclass=lazy struct; Pydantic=strict validator; types=labels. Prefer composition, frozen dataclasses for keys, Pydantic at API boundary.
