"""Solution: conductor runs forward, undoes backward."""

STEPS = ["pay", "stock", "ship"]


def run(order, fail_at=None):
    done = []
    for name in STEPS:
        if name == fail_at:
            return f"failed:{name}", [n for n, _ in reversed(done)]
        done.append((name, order))
    return "done", []


def compensated_names(result):
    return result[1]
