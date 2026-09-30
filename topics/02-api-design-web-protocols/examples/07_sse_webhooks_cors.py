"""07_sse_webhooks_cors.py — live score ticker (SSE) + society gate (CORS).

Run: uv run python topics/02-api-design-web-protocols/examples/07_sse_webhooks_cors.py
Spins a real localhost SSE server, streams 3 tokens, parses them like an LLM client.
"""

import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKENS = ["Namaste", " from", " the API!"]


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        body = "".join(f"data: {t}\n\n" for t in TOKENS) + "data: [DONE]\n\n"
        raw = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

# SSE client: read stream, split on blank lines, collect data: lines
text = urllib.request.urlopen(f"http://127.0.0.1:{port}/stream").read().decode()
got = [ln[6:] for blk in text.split("\n\n") for ln in blk.splitlines() if ln.startswith("data: ")]
srv.shutdown()
print("streamed:", got)
assert got == [*TOKENS, "[DONE]"], got


# --- CORS preflight checker (society gate logic) ---
def preflight_ok(origin, method, req_headers, allowed_origin, allowed_methods, allowed_headers):
    if allowed_origin != "*" and origin != allowed_origin:
        return False, "origin not allowed"
    if method not in allowed_methods:
        return False, "method not allowed"
    if any(h.lower() not in [a.lower() for a in allowed_headers] for h in req_headers):
        return False, "header not allowed"
    return True, "ok"


ok, _ = preflight_ok(
    "https://frontend.com",
    "PATCH",
    ["Authorization"],
    "https://frontend.com",
    ["GET", "POST", "PATCH"],
    ["Authorization", "Content-Type"],
)
assert ok
bad, why = preflight_ok(
    "https://evil.com",
    "PATCH",
    ["Authorization"],
    "https://frontend.com",
    ["GET", "POST", "PATCH"],
    ["Authorization", "Content-Type"],
)
assert not bad and "origin" in why


# --- Cookie builder with 3 safety stamps ---
def cookie(name, val):
    return f"{name}={val}; HttpOnly; Secure; SameSite=Lax; Max-Age=3600; Path=/"


c = cookie("session", "abc")
assert all(k in c for k in ("HttpOnly", "Secure", "SameSite=Lax"))
print("OK — SSE data: chunks + [DONE]; CORS mirrors exact origin; cookies HttpOnly+Secure")
