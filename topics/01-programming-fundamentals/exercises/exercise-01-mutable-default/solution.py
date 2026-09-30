"""Solution: never use mutable default; use None."""


def add_student_bad(name, box=[]):  # noqa: B006 — intentional trap demo
    box.append(name)
    return box


def add_student(name, box=None):
    if box is None:
        box = []
    box.append(name)
    return box
