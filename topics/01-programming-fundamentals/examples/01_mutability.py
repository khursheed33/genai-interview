"""01_mutability.py — school bag (mutable) vs sealed gift (immutable).

Run: uv run python topics/01-programming-fundamentals/examples/01_mutability.py
Expected: shows shared-list trap and the None-fix.
"""

# Mutable: same bag shared
bag = [1, 2]
same_bag = bag
bag.append(3)
print("shared bag:", bag, same_bag)  # [1,2,3] [1,2,3]
assert bag == [1, 2, 3] and same_bag == [1, 2, 3]


# Immutable: new sticker each time
name = "ram"
other = name
name = name + "a"
print("immutable str:", name, "| other still:", other)  # rama | ram
assert name == "rama" and other == "ram"


# Real-world trap: mutable default arg = one register for two classes
def add_bad(item, box=[]):  # noqa: B006 — intentional demo of the trap
    box.append(item)
    return box


print("trap:", add_bad("a"), add_bad("b"))  # ['a'] then ['a','b'] — leaked!


def add_good(item, box=None):
    box = box if box is not None else []
    box.append(item)
    return box


print("fixed:", add_good("a"), add_good("b"))  # ['a'] ['b']
assert add_good("a") == ["a"] and add_good("b") == ["b"]
print("OK — use None as default, never [] / {}")
