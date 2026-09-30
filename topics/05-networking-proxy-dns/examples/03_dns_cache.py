"""03_dns_cache.py — phonebook packet + TTL memory (offline-safe).

Run: uv run python topics/05-networking-proxy-dns/examples/03_dns_cache.py
"""

import socket
import struct
import time

RECORDS = {
    "A": 1,
    "AAAA": 28,
    "CNAME": 5,
    "MX": 15,
    "TXT": 16,
    "NS": 2,
    "SRV": 33,
    "PTR": 12,
    "SOA": 6,
}
assert RECORDS["A"] == 1 and RECORDS["AAAA"] == 28


def build_query(name, qtype="A"):
    header = struct.pack(">HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0)  # id, RD flag, QD=1
    qname = b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\x00"
    return header + qname + struct.pack(">HH", RECORDS[qtype], 1)


def parse_qname(pkt):
    labels, i = [], 12  # skip 12-byte header
    while pkt[i] != 0:
        n = pkt[i]
        labels.append(pkt[i + 1 : i + 1 + n].decode())
        i += 1 + n
    return ".".join(labels)


pkt = build_query("api.shop.com")
assert parse_qname(pkt) == "api.shop.com"
print("DNS packet: built + parsed locally (header + labels + QTYPE/QCLASS)")


class TTLCache:  # recursive resolver's memory: remember answers for TTL seconds
    def __init__(self, clock=time.time):
        self.clock, self.store = clock, {}

    def put(self, name, value, ttl):
        self.store[name] = (value, self.clock() + ttl)

    def get(self, name):
        hit = self.store.get(name)
        if not hit or hit[1] <= self.clock():
            self.store.pop(name, None)
            return None  # expired or negative-cache miss -> walk again
        return hit[0]


now = {"t": 1000.0}
cache = TTLCache(clock=lambda: now["t"])
cache.put("api.shop.com", "203.0.113.7", ttl=300)
assert cache.get("api.shop.com") == "203.0.113.7"
now["t"] += 301
assert cache.get("api.shop.com") is None  # TTL died -> re-resolve
print("TTL cache: hit within 300s, miss after (lower TTL a day BEFORE migrations!)")

# localhost always resolves — proves resolver path without internet
assert socket.gethostbyname("localhost") == "127.0.0.1"
print("OK — A=address CNAME=nickname MX=mail TXT=proofs; cache honors TTL")
