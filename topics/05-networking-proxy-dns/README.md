# 05 - Networking, Proxy, DNS

> Scope: README.md section 5: OSI/TCP-IP, DNS records/flow, hosts/CoreDNS, forward/reverse proxy (Nginx/Envoy), LB L4/L7, CDN, VPC/VPN, debugging tools
> Main checklist: [`../../README.md`](../../README.md)

## Goals
- [ ] Understand core concepts and trade-offs
- [ ] Hands-on practice in `examples/`
- [ ] Solve tasks in `exercises/`
- [ ] Capture learnings in `notes/`
- [ ] Answer `interview-questions.md` confidently

## What to learn (all covered — read notes in order)
- TCP/IP → `notes/01-tcp-ip-foundation.md` (OSI/TCP-IP, TCP vs UDP, handshake, ports/sockets)
- Subnets → `notes/02-subnets-nat-vpc.md` (CIDR, routing, NAT, SG/NACL/bastion/VPN)
- DNS → `notes/03-dns.md` (9 records, TTL, resolution walk, split-horizon, custom domains)
- Proxies → `notes/04-proxies.md` (forward/reverse, nginx 15-liner, corp proxy env/PAC)
- LB/CDN → `notes/05-lb-cdn.md` (L4 vs L7, 5 algorithms, health/sticky/TLS, edge cache)
- Tunnels → `notes/06-tunnels-mesh.md` (-L/-R/-D/k8s, discovery, Istio/Linkerd)
- Debug → `notes/07-debugging.md` (symptom→tool table, corporate classics)

## Examples (7 runnable — verified, live localhost sockets)
| File | Covers | Run |
|---|---|---|
| `examples/01_tcp_udp_sockets.py` | TCP echo, UDP postcard, port probe | `uv run python topics/05-networking-proxy-dns/examples/01_tcp_udp_sockets.py` |
| `examples/02_cidr_subnets.py` | VPC math, tier split, NAT table | same pattern |
| `examples/03_dns_cache.py` | packet build/parse, TTL cache, localhost resolve | same pattern |
| `examples/04_reverse_proxy.py` | backend + proxy, XFF/X-Request-ID, failover | same pattern |
| `examples/05_load_balancer.py` | RR/weighted/least-conn/hash/sticky/health | same pattern |
| `examples/06_tunnel_cmds.py` | validated -L/-R/-D/k8s builders | same pattern |
| `examples/07_debug_probes.js` | dns.lookup + nc + curl timings | `node .../07_debug_probes.js` |

## Exercises (5 — `uv run pytest topics/05-networking-proxy-dns/exercises -q`, 10 tests)
- `exercise-01-cidr-plan` — usable count, contains, even carve
- `exercise-02-dns-cache` — 9 record types + TTL memory
- `exercise-03-proxy-headers` — XFF chain + sick-upstream skip
- `exercise-04-lb-pickers` — RR/least-conn/hash/health/sticky
- `exercise-05-tunnel-debug` — validated builders + symptom router

## Structure
- `README.md` - this checklist entry point
- `notes/` - your condensed notes (add `.md` per sub-topic)
- `examples/` - runnable minimal examples (python/js/sh)
- `exercises/` - practice tasks + solutions
- `interview-questions.md` - Q and A bank

## How to use
1. Read the checklist item in root README.
2. Add notes + code + diagrams here.
3. Do 2-3 exercises and 1 mini-project link in `projects/` if applicable.
4. Self-quiz with interview questions.

## Resources
- Add links as you learn (docs, papers, videos).
- Prefer primary sources: official docs, RFCs, papers.

## Progress
- [x] Notes drafted (7 files, postcard/society/phonebook stories)
- [x] Examples run (7 files, verified: live sockets + proxy + node)
- [x] Exercises done (5 exercises, 10 pytest tests green)
- [x] Interview Qs revised (20+ Q/A in `interview-questions.md`)
