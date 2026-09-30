"""Solution: yield = pause-and-resume tap."""


def line_stream(n):
    for i in range(n):
        yield f"order-{i}"


def active_orders(lines):
    for line in lines:
        if not line.startswith("CANCELLED"):
            yield line
