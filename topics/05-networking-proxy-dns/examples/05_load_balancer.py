"""05_load_balancer.py — counter tokens, shortest queue, sticky regulars.

Run: uv run python topics/05-networking-proxy-dns/examples/05_load_balancer.py
"""

import hashlib

NODES = ["a", "b", "c"]


def round_robin(nodes, n):
    return [nodes[i % len(nodes)] for i in range(n)]


assert round_robin(NODES, 7) == ["a", "b", "c", "a", "b", "c", "a"]
print("RR: a b c a b c a")


def weighted_rr(nodes_weights, n):
    bag = [node for node, w in nodes_weights for _ in range(w)]
    return [bag[i % len(bag)] for i in range(n)]


assert weighted_rr([("a", 3), ("b", 1)], 4) == ["a", "a", "a", "b"]
print("weighted: big box 'a' takes 3/4 (weight 0 drains a node!)")


def least_conn(active: dict):
    return min(active, key=lambda k: active[k])


assert least_conn({"a": 5, "b": 2, "c": 9}) == "b"
print("least-conn: 'b' has shortest queue (use for WS/LLM streams!)")


def ip_hash(ip, nodes):
    return nodes[int(hashlib.md5(ip.encode()).hexdigest(), 16) % len(nodes)]


assert ip_hash("1.2.3.4", NODES) == ip_hash("1.2.3.4", NODES)  # stable per street
print("ip-hash: same street, same counter (caches love this)")


def healthy(nodes, is_up):
    live = [n for n in nodes if is_up.get(n, True)]
    assert live, "zero healthy -> 503 + Retry-After (shed, don't queue forever!)"
    return live


assert healthy(NODES, {"a": True, "b": False, "c": True}) == ["a", "c"]


class Sticky:  # cookie-pinned regulars (last resort — prefer stateless!)
    def __init__(self):
        self.pins = {}

    def route(self, user, nodes):
        return self.pins.setdefault(user, nodes[hash(user) % len(nodes)])


s = Sticky()
assert s.route("asha", NODES) == s.route("asha", NODES)
print("OK — RR for equals, weighted to drain, least-conn for streams, hash for caches")
