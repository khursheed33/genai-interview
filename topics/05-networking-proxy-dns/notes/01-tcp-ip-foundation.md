# 01 — TCP/IP Foundation: Postcards, Phone Calls & Door Numbers

## 1. OSI vs TCP/IP (7 suits vs 4 practical layers)

| TCP/IP | OSI approx | Job | Example |
|---|---|---|---|
| Link | Physical + Data Link | wires/WiFi frames, MAC | Ethernet, ARP ("who has 10.0.0.5?") |
| Internet | Network | addresses + routing across networks | **IP**, ICMP (ping), `ip route` |
| Transport | Transport | ports + reliability choice | **TCP** (phone call) vs **UDP** (postcard) |
| Application | Session/Presentation/Application | what users want | HTTP, DNS, TLS, gRPC |

Interview line: **"Routers stop at L3, load balancers live at L4/L7, TLS glues between transport and app."**

## 2. TCP (phone call) vs UDP (postcard)

| | TCP | UDP |
|---|---|---|
| Story | Call: "hello? hello? ok, order 3 dosas" (ack every line) | Postcard: fire-and-forget, may duplicate/lose/reorder |
| Guarantees | order + no-loss + no-dupe (seq/ack + retransmit) | none (app handles: QUIC, RTP, game netcode) |
| Cost | handshake + head-of-line blocking | 1 packet, lowest latency |
| Use | HTTP/1-2, Postgres, SSH | DNS, DHCP, streaming, HTTP/3's foundation (QUIC) |

## 3. 3-way handshake (the knock ritual) + teardown

```
you: SYN (seq=100) ──────────────→ server   "may I talk? starting at 100"
you: ←──────── SYN-ACK (seq=300, ack=101)    "sure! I'm at 300, got your 101"
you: ACK (ack=301) ──────────────→ server   "got it — line open!"
... data with seq/ack ... FIN/FIN-ACK closes politely; RST hangs up rudely
```

- **SYN flood**: attacker sends SYNs, never ACKs → backlog fills → real users blocked. Lock: SYN cookies + backlog tuning + SYN-proxy at edge.
- `ss -tlnp` shows LISTEN doors; `ESTABLISHED` = open calls; `TIME_WAIT` = recently hung up (port reuse delay — why load tests hit "address in use").

## 4. Ports + sockets (building + flat numbers)

- **Port** 16-bit (0–65535): 0–1023 privileged (80 HTTP, 443 HTTPS, 22 SSH, 53 DNS, 5432 PG), 1024–49151 registered (6379 Redis, 6333 Qdrant), 49152+ ephemeral (your browser's side).
- **Socket** = `IP:port` + protocol. Server binds `0.0.0.0:8000` (all doors) vs `127.0.0.1:8000` (localhost only — safer for debug UIs!). Client gets ephemeral port per connection (that's why 40k browser tabs work).
- NAT (topic note 02) rewrites these; proxies (note 04) terminate and re-open them.

Runnable: real localhost TCP echo + UDP + port probe in `../examples/01_tcp_udp_sockets.py`.
