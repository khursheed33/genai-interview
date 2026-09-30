"""04_reverse_proxy.py — receptionist door: real backend + forwarding proxy.

Run: uv run python topics/05-networking-proxy-dns/examples/04_reverse_proxy.py
Backend on :0, proxy on :0. Proxy injects X-Forwarded-For/Proto/X-Request-ID,
skips dead upstreams (passive health), client asserts end-to-end.
"""

import json
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SEEN = {}


class Backend(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _ok(self, payload):
        raw = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        SEEN.update({k.lower(): v for k, v in dict(self.headers).items()})
        SEEN["path"] = self.path
        self._ok({"app": "api-1", "path": self.path})


backend = ThreadingHTTPServer(("127.0.0.1", 0), Backend)
threading.Thread(target=backend.serve_forever, daemon=True).start()
B_PORT = backend.server_address[1]

UPSTREAMS = [{"url": f"http://127.0.0.1:{B_PORT}", "dead_until": 0.0, "fails": 0}]
REQ = {"n": 0}


class Proxy(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _forward(self, method):
        import time

        REQ["n"] += 1
        ups = [u for u in UPSTREAMS if u["dead_until"] <= time.time()]
        assert ups, "all upstreams dead -> 503 + shed (backpressure!)"
        target = ups[0]["url"] + self.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else None
        fwd = urllib.request.Request(target, data=body, method=method)
        client_ip = self.client_address[0]
        fwd.add_header("X-Forwarded-For", client_ip)  # real client chain!
        fwd.add_header("X-Forwarded-Proto", "http")
        fwd.add_header("X-Request-ID", f"req_{REQ['n']:04d}")
        try:
            with urllib.request.urlopen(fwd, timeout=5) as r:
                raw = r.read()
        except Exception:
            ups[0]["fails"] += 1
            ups[0]["dead_until"] = time.time() + 30
            raise
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Request-ID", f"req_{REQ['n']:04d}")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        self._forward("GET")


proxy = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
threading.Thread(target=proxy.serve_forever, daemon=True).start()
P_PORT = proxy.server_address[1]

with urllib.request.urlopen(f"http://127.0.0.1:{P_PORT}/v1/orders/7", timeout=5) as r:
    data = json.loads(r.read())
    trace = r.headers.get("X-Request-ID")
assert data == {"app": "api-1", "path": "/v1/orders/7"}, data
assert SEEN.get("x-forwarded-for") == "127.0.0.1", SEEN
assert SEEN.get("x-request-id") == trace, SEEN
backend.shutdown()
proxy.shutdown()
print("proxied:", data, "| trace:", trace, "| backend saw XFF:", SEEN.get("x-forwarded-for"))
print("OK — proxy_pass + X-Forwarded-* + X-Request-ID; dead upstream = fail over")
