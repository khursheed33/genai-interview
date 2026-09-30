"""Solution: leader runs, followers wait on an Event; errors never cached."""

import threading


class Flight:
    def __init__(self):
        self.lock = threading.Lock()
        self.inflight = {}

    def get(self, key, fn):
        with self.lock:
            if key in self.inflight:
                ev, box = self.inflight[key]
                leader = False
            else:
                ev, box = threading.Event(), {}
                self.inflight[key] = (ev, box)
                leader = True
        if not leader:
            ev.wait()
            if "err" in box:
                raise box["err"]
            return box["val"]
        try:
            box["val"] = fn()
            return box["val"]
        except Exception as e:
            box["err"] = e
            raise
        finally:
            with self.lock:
                del self.inflight[key]
            ev.set()
