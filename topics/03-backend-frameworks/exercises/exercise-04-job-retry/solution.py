"""Solution: retry loop + idempotency set + DLQ list."""


def run_with_retry(fn, max_tries=3):
    last = None
    for attempt in range(1, max_tries + 1):
        try:
            return fn(), attempt
        except Exception as e:
            last = e
    raise last


def process_once(job_id, fn, done: set, dlq: list, max_tries=3):
    if job_id in done:
        return "duplicate"
    try:
        run_with_retry(fn, max_tries)
    except Exception as e:
        dlq.append((job_id, str(e)))
        return "failed"
    done.add(job_id)
    return "done"
