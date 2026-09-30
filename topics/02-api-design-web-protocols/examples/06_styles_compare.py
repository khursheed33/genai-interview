"""06_styles_compare.py — phone call vs deed vs walkie-talkie vs doorbell.

Run: uv run python topics/02-api-design-web-protocols/examples/06_styles_compare.py
"""

import hashlib
import hmac

# --- GraphQL N+1 vs DataLoader (count the queries!) ---
QUERIES = {"n": 0}
ITEMS_DB = {i: [f"item-{i}-a", f"item-{i}-b"] for i in range(1, 6)}


def fetch_items_naive(order_id):
    QUERIES["n"] += 1
    return ITEMS_DB[order_id]


def fetch_items_batched(order_ids):
    QUERIES["n"] += 1  # ONE query with WHERE id IN (...)
    return [ITEMS_DB[i] for i in order_ids]


orders = [1, 2, 3, 4, 5]
QUERIES["n"] = 0
_ = [fetch_items_naive(o) for o in orders]
print("naive N+1 queries:", QUERIES["n"])  # 5
QUERIES["n"] = 0
_ = fetch_items_batched(orders)
print("dataloader batched queries:", QUERIES["n"])  # 1
assert QUERIES["n"] == 1

# --- SOAP envelope (see once, recognize in legacy banks) ---
SOAP = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body><GetOrder><id>101</id></GetOrder></soap:Body></soap:Envelope>"""
assert "Envelope" in SOAP and "Body" in SOAP
print("SOAP = Envelope>Body, WSDL contract, Fault errors, WS-Security")

# --- Webhook HMAC verify (doorbell with secret knock) ---
SECRET = b"hook-secret"


def sign(body: bytes) -> str:
    return hmac.new(SECRET, body, hashlib.sha256).hexdigest()


def verify(body: bytes, sig: str) -> bool:
    return hmac.compare_digest(sign(body), sig)


body = b'{"event":"paid","id":101}'
assert verify(body, sign(body)) and not verify(b"tampered", sign(body))
print("webhook HMAC ok (compare_digest, respond 200 fast, queue heavy work)")


# --- Style picker (the interview answer as a function) ---
def pick(need):
    return {
        "crud-public": "REST (cacheable URLs + OpenAPI)",
        "exact-fields-mobile": "GraphQL (+DataLoader, depth limits)",
        "internal-streams": "gRPC (protobuf, bidi streaming)",
        "token-push": "SSE (text/event-stream, auto-reconnect)",
        "two-way-live": "WebSockets (101 Switching)",
        "event-notify": "webhooks (HMAC, 200 fast, DLQ)",
    }[need]


assert "gRPC" in pick("internal-streams")
print("OK — GraphQL needs DataLoader; webhooks need HMAC; streams need HTTP/2")
