"""08_middleware.py — conveyor-belt chefs (onion model).

Run: uv run python topics/02-api-design-web-protocols/examples/08_middleware.py
"""

import time
import uuid

LOG = []


def mw_request_id(req, nxt):
    req["id"] = req["headers"].get("X-Request-ID", f"req_{uuid.uuid4().hex[:8]}")
    return nxt(req)


def mw_auth(req, nxt):
    if req["headers"].get("Authorization") != "Bearer good-token":
        return {"status": 401, "body": {"title": "Unauthorized", "traceId": req.get("id", "?")}}
    return nxt(req)


def mw_logger(req, nxt):
    t0 = time.perf_counter()
    res = nxt(req)
    ms = (time.perf_counter() - t0) * 1000
    LOG.append(f"{req['method']} {req['path']} -> {res['status']} [{req['id']}] {ms:.1f}ms")
    res["headers"] = {"X-Request-ID": req["id"]}
    return res


def build_chain(*mws):
    def run(req, handler):
        nxt = handler
        for m in reversed(mws):  # first listed = outermost chef
            inner, current = nxt, m

            def nxt(r, _inner=inner, _m=current):
                return _m(r, _inner)

        return nxt(req)

    return run


def handler(req):
    if req["path"] == "/orders/101":
        return {"status": 200, "body": {"id": 101}}
    return {"status": 404, "body": {"title": "Not found"}}


chain = build_chain(mw_request_id, mw_auth, mw_logger)
ok = chain(
    {"method": "GET", "path": "/orders/101", "headers": {"Authorization": "Bearer good-token"}},
    handler,
)
no = chain({"method": "GET", "path": "/orders/101", "headers": {}}, handler)
print(ok["status"], ok["headers"], "| unauth:", no["status"])
assert ok["status"] == 200 and "X-Request-ID" in ok["headers"]
assert no["status"] == 401
assert LOG and "req_" in LOG[0]
print("LOG:", LOG[0])
print("OK — order: trace -> auth -> log; auth before billable work; trace ID everywhere")
