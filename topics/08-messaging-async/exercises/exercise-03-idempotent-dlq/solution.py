"""Solution: id-set dedupes, retries bounded, poison parked."""


def handler(body):
    if body == "poison":
        raise RuntimeError("rotten mango")
    return f"ok:{body}"


def consume(messages, max_tries=3):
    seen, done_ids, duplicates, dlq = set(), [], [], []
    runs = {"n": 0}
    for m in messages:
        if m["id"] in seen:
            duplicates.append(m["id"])
            continue
        ok = False
        for _ in range(max_tries):
            runs["n"] += 1
            try:
                handler(m["body"])
                ok = True
                break
            except Exception:
                continue
        if ok:
            seen.add(m["id"])
            done_ids.append(m["id"])
        else:
            dlq.append({"id": m["id"], "tries": max_tries, "error": "rotten mango"})
    return done_ids, duplicates, dlq, runs["n"]
