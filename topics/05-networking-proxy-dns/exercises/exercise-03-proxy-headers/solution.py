"""Solution: stamp the real client, skip the sick."""


def forward_headers(client_ip, proto="http", req_id="req_1", existing=None):
    xff = f"{existing}, {client_ip}" if existing else client_ip
    return {"X-Forwarded-For": xff, "X-Forwarded-Proto": proto, "X-Request-ID": req_id}


def pick(upstreams, now=0.0):
    for u in upstreams:
        if u["dead_until"] <= now:
            return u
    raise RuntimeError("no healthy upstream")
