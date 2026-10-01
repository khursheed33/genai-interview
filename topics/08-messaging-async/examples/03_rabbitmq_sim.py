"""03_rabbitmq_sim.py — smart postmen: direct/fanout/topic + ack discipline.

Run: uv run python topics/08-messaging-async/examples/03_rabbitmq_sim.py
"""


def topic_match(pattern, key):
    pp, kp = pattern.split("."), key.split(".")
    if "#" in pp:  # '#' swallows the REST (must be last here — AMQP allows mid too!)
        i = pp.index("#")
        return pp[:i] == kp[:i]
    if len(pp) != len(kp):
        return False
    return all(p == "*" or p == k for p, k in zip(pp, kp, strict=True))


assert topic_match("order.*.blr", "order.paid.blr")
assert not topic_match("order.*.blr", "order.paid.del")
assert topic_match("order.#", "order.paid.blr.extra")
print("topic patterns: * one word, # rest")


class Broker:
    def __init__(self):
        self.bindings = []  # (exchange, kind, pattern, queue)
        self.queues = {}
        self.unacked = {}

    def bind(self, ex, kind, pattern, queue):
        self.bindings.append((ex, kind, pattern, queue))
        self.queues.setdefault(queue, [])

    def publish(self, ex, key, msg):
        for e, kind, pattern, q in self.bindings:
            if e != ex:
                continue
            hit = (
                kind == "fanout"
                or (kind == "direct" and pattern == key)
                or (kind == "topic" and topic_match(pattern, key))
            )
            if hit:
                self.queues[q].append({"key": key, "msg": msg, "tries": 0})

    def get(self, queue, prefetch=1):
        if len(self.unacked.get(queue, [])) >= prefetch:
            return None  # fair share! (basic.qos)
        if not self.queues[queue]:
            return None
        m = self.queues[queue].pop(0)
        self.unacked.setdefault(queue, []).append(m)
        return m

    def ack(self, queue, m):
        self.unacked[queue].remove(m)  # AFTER work!

    def nack_requeue(self, queue, m):
        self.unacked[queue].remove(m)
        m["tries"] += 1
        self.queues[queue].append(m)


b = Broker()
b.bind("shop", "fanout", "", "audit")  # broadcast!
b.bind("shop", "topic", "order.#", "orders")
b.bind("shop", "direct", "pay", "payments")
b.publish("shop", "order.paid.blr", "o7")
assert [m["msg"] for m in b.queues["audit"]] == ["o7"]
assert [m["msg"] for m in b.queues["orders"]] == ["o7"]
assert b.queues["payments"] == []
print("fanout heard all, topic matched order.#, direct pay silent")

m = b.get("orders")
assert b.get("orders", prefetch=1) is None  # 1 unacked = at cap!
b.ack("orders", m)
assert b.get("orders") is None  # acked + empty
print("OK — exchanges sort, manual-ack after work, prefetch = fair share + backpressure")
