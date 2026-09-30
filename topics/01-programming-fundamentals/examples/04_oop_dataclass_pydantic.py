"""04_oop_dataclass_pydantic.py — biscuit mould, pre-printed form, strict guard.

Run: uv run python topics/01-programming-fundamentals/examples/04_oop_dataclass_pydantic.py
"""

from dataclasses import dataclass, field

from pydantic import BaseModel, Field, ValidationError


class Cart:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"Cart({self.items!r})"


c = Cart([1, 2, 3])
print(c, "| len:", len(c))  # Cart([1, 2, 3]) | len: 3
assert len(c) == 3


@dataclass(frozen=True)
class User:
    id: int
    name: str
    tags: list[str] = field(default_factory=list)


u = User(id=1, name="asha")
print(u)
assert u.tags == []


class OrderIn(BaseModel):
    id: int = Field(gt=0)
    email: str
    items: list[str] = Field(min_length=1)


good = OrderIn(id=1, email="a@x.com", items=["dosa"])
print("valid:", good.model_dump())

try:
    OrderIn(id=-1, email="x", items=[])
except ValidationError as e:
    print("caught invalid order, errors:", len(e.errors()))
print("OK — dataclass for structs, pydantic at API boundary")
