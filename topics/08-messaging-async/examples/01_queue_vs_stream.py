"""01_queue_vs_stream.py — counter vs loudspeaker vs diary (same events, 3 promises).

Run: uv run python topics/08-messaging-async/examples/01_queue_vs_stream.py
"""

# --- queue: competing consumers, ONE takes each ---
import queue

q: queue.Queue = queue.Queue()
for m in ["m1", "m2", "m3", "m4"]:
    q.put(m)
taken = {"w1": [], "w2": []}
for w in ["w1", "w2"] * 2:
    taken[w].append(q.get())
assert sorted(taken["w1"] + taken["w2"]) == ["m1", "m2", "m3", "m4"]
assert len(taken["w1"]) == 2  # split, never doubled!
print("queue: each message exactly ONE worker", taken)


# --- pub/sub: EVERY subscriber hears ---
class Bus:
    def __init__(self):
        self.subs = {}

    def sub(self, topic, fn):
        self.subs.setdefault(topic, []).append(fn)

    def pub(self, topic, msg):
        for fn in self.subs.get(topic, []):
            fn(msg)


heard = {"warehouse": [], "email": []}
bus = Bus()
bus.sub("paid", heard["warehouse"].append)
bus.sub("paid", heard["email"].append)
bus.pub("paid", "order:7")
assert heard == {"warehouse": ["order:7"], "email": ["order:7"]}
print("pub/sub: BOTH services heard (late joiner would miss — that's streams' job!)")


# --- log: numbered diary, replay from any offset ---
class Log:
    def __init__(self):
        self.records = []

    def append(self, v):
        self.records.append(v)
        return len(self.records) - 1  # offset!

    def read_from(self, offset):
        return self.records[offset:]


log = Log()
offsets = [log.append(f"e{i}") for i in range(5)]
assert log.read_from(0) == [f"e{i}" for i in range(5)]  # new service replays ALL
assert log.read_from(3) == ["e3", "e4"]  # crash recovery resumes!
print("log: offsets", offsets, "-> replay from 0 or resume from 3")
print("OK — compete=queue, broadcast=pub/sub, replay=log (SNS fans out to SQS!)")
