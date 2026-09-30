# Exercise 01 — Fix the Shared Tiffin (mutable default)

**Story:** Two classes share one attendance register. Adding Asha to Class A also shows her in Class B. Fix it.

## Task
In `solution.py`, `add_student_bad` uses `box=[]`. Write `add_student(name, box=None)` that returns a NEW list each call when no box given.

## Acceptance
- `add_student("a") == ["a"]`, second call `add_student("b") == ["b"]` (no leak)
- Passing own list appends to it: `add_student("c", ["x"]) == ["x", "c"]`
- Run: `uv run pytest topics/01-programming-fundamentals/exercises/exercise-01-mutable-default -q`
