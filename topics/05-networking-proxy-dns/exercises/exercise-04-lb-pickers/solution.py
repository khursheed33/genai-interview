"""Solution: tokens, shortest queue, stable hash, health gate, pins."""

import hashlib


def rr(nodes, n):
    return [nodes[i % len(nodes)] for i in range(n)]


def least_conn(active: dict):
    return min(active, key=lambda k: active[k])


def ip_hash(ip, nodes):
    return nodes[int(hashlib.md5(ip.encode()).hexdigest(), 16) % len(nodes)]


def healthy(nodes, is_up: dict):
    live = [n for n in nodes if is_up.get(n, True)]
    if not live:
        raise RuntimeError("no healthy node")
    return live


class Sticky:
    def __init__(self):
        self.pins = {}

    def route(self, user, nodes):
        return self.pins.setdefault(user, nodes[hash(user) % len(nodes)])
