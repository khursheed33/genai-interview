"""07_sourcing_cqrs.py — diary IS the truth: fold, snapshot, time-travel, project.

Run: uv run python topics/08-messaging-async/examples/07_sourcing_cqrs.py
"""

EVENTS = [("credited", 50), ("debited", 30), ("credited", 20)]


def fold(events):
    bal = 0
    for kind, amt in events:
        bal += amt if kind == "credited" else -amt
    return bal


assert fold(EVENTS) == 40
assert fold(EVENTS[:2]) == 20  # time-travel: balance last Tuesday!
print("fold all = 40 | fold [:2] = 20 (audit + time-travel free!)")

SNAPSHOTS = {2: 20}  # version -> balance (cache every Nth!)


def balance_at(version):
    snap_v = max((v for v in SNAPSHOTS if v <= version), default=0)
    return SNAPSHOTS.get(snap_v, 0) + fold(EVENTS[snap_v:version])


assert balance_at(3) == 40 and balance_at(2) == 20
print("snapshot@2 + fold 1 event = fast read (no 1M-event replays!)")


# CQRS projection: read model per view (denormalized dashboard!)
def project_dashboard(events):
    return {
        "n_credits": sum(1 for k, _ in events if k == "credited"),
        "total_in": sum(a for k, a in events if k == "credited"),
    }


assert project_dashboard(EVENTS) == {"n_credits": 2, "total_in": 70}
print("projection:", project_dashboard(EVENTS))
print("OK — append events, fold for truth, snapshot for speed, project per view!")
