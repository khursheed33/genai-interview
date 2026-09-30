"""04_tasks_queue.py — kitchen helpers: 202 now, curry later (retry + DLQ).

Run: uv run python topics/03-backend-frameworks/examples/04_tasks_queue.py
No Redis needed: stdlib queue + thread stand in for Celery/RQ/BullMQ.
"""

import queue
import threading
import time

JOBS, DLQ, DONE = {}, [], {}
Q: queue.Queue = queue.Queue()
SEEN_IDS = set()  # idempotency: same job_id twice = one effect


def submit(job_id, payload):
    JOBS[job_id] = {"status": "pending", "tries": 0}
    Q.put((job_id, payload))
    return {"job_id": job_id, "status_url": f"/jobs/{job_id}"}, 202


def worker(flaky_first=True):
    while True:
        try:
            job_id, payload = Q.get(timeout=0.2)
        except queue.Empty:
            return
        if job_id in SEEN_IDS:  # duplicate delivery -> skip, already done
            Q.task_done()
            continue
        JOBS[job_id]["tries"] += 1
        try:
            if flaky_first and JOBS[job_id]["tries"] == 1:
                raise RuntimeError("pdf parser hiccup")
            time.sleep(0.01)
            DONE[job_id] = f"summary of {payload}"
            JOBS[job_id]["status"] = "done"
            SEEN_IDS.add(job_id)
        except Exception as e:
            if JOBS[job_id]["tries"] >= 3:
                JOBS[job_id]["status"] = "failed"
                DLQ.append((job_id, str(e)))  # poison parked + alert
            else:
                time.sleep(0.01 * 2 ** JOBS[job_id]["tries"])  # backoff
                Q.put((job_id, payload))  # requeue
        finally:
            Q.task_done()


body, code = submit("job_77", "50-page menu PDF")
assert code == 202 and body["status_url"] == "/jobs/job_77"
t = threading.Thread(target=worker, daemon=True)
t.start()
Q.join()
assert JOBS["job_77"]["status"] == "done" and JOBS["job_77"]["tries"] == 2
assert DONE["job_77"].startswith("summary")
# duplicate delivery processed once
Q.put(("job_77", "50-page menu PDF"))
Q.join()
assert JOBS["job_77"]["tries"] == 2
print("job:", JOBS["job_77"], "| DLQ:", DLQ)
print("OK — 202 + job row + idempotent worker + retry/backoff + DLQ")
