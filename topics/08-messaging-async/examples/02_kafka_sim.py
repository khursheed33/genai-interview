"""02_kafka_sim.py — library ledger: partitions, groups, compaction (pure python).

Run: uv run python topics/08-messaging-async/examples/02_kafka_sim.py
"""

import hashlib


class Topic:
    def __init__(self, name, partitions):
        self.name = name
        self.parts = [[] for _ in range(partitions)]

    def publish(self, key, value):
        p = int(hashlib.md5(key.encode()).hexdigest(), 16) % len(self.parts)
        self.parts[p].append((key, value))
        return p, len(self.parts[p]) - 1  # partition + offset!


t = Topic("orders", 4)
assert t.publish("asha", "o1")[0] == t.publish("asha", "o2")[0]  # same key, same shelf!
print("keys route: asha always same partition (order per key!)")


def assign(partitions, consumers):  # group rebalance: deal shelves round-robin
    return {
        c: [p for i, p in enumerate(partitions) if i % len(consumers) == consumers.index(c)]
        for c in consumers
    }


assert assign([0, 1, 2, 3], ["c1", "c2"]) == {"c1": [0, 2], "c2": [1, 3]}
print("rebalance 4 shelves / 2 clerks:", assign([0, 1, 2, 3], ["c1", "c2"]))


# offsets: commit AFTER work (at-least!) — crash replays, idempotency saves (note 04!)
committed = {}


def consume_group(topic, group, assignment, process):
    for _consumer, parts in assignment.items():
        for p in parts:
            start = committed.get((group, p), 0)
            for offset in range(start, len(topic.parts[p])):
                process(topic.parts[p][offset])
                committed[(group, p)] = offset + 1  # bookmark AFTER success


seen = []
consume_group(t, "g1", {"c1": [0, 1, 2, 3]}, lambda rec: seen.append(rec))
assert len(seen) == sum(len(p) for p in t.parts)
print("offsets committed after work:", committed)


# compaction: keep LAST value per key (changelog forever!)
def compact(records):
    latest = {}
    for k, v in records:
        latest[k] = v
    return latest


assert compact([("u1", "blr"), ("u2", "del"), ("u1", "mum")]) == {"u1": "mum", "u2": "del"}
print("OK — key->partition (order!), rebalance deals, offsets bookmark, compact keeps latest")
