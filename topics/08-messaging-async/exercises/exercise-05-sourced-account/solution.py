"""Solution: fold is truth, snapshots are shortcuts."""


def apply_one(bal, ev):
    kind, amt = ev
    return bal + amt if kind == "credit" else bal - amt


def fold(events):
    bal = 0
    for ev in events:
        bal = apply_one(bal, ev)
    return bal


def with_snapshot(events, every=2):
    snaps, bal = {}, 0
    for i, ev in enumerate(events, 1):
        bal = apply_one(bal, ev)
        if i % every == 0:
            snaps[i] = bal
    return snaps


def balance_at(events, snapshots, version):
    snap_v = max((v for v in snapshots if v <= version), default=0)
    bal = snapshots.get(snap_v, 0)
    for ev in events[snap_v:version]:
        bal = apply_one(bal, ev)
    return bal
