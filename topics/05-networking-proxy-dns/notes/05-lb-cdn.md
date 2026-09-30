# 05 — Load Balancing & CDN: Counters, Bouncers & Photocopy Shops

## 1. L4 vs L7 (which floor does the bouncer read?)

| | L4 (TCP/UDP) | L7 (HTTP) |
|---|---|---|
| Sees | IP + port only | URL, headers, cookies, auth, body hints |
| Routes by | IP hash, ports | path (`/api→a, /static→b`), header, JWT claim, gRPC method |
| TLS | passes through (app terminates) | terminates (cert HERE, re-encrypt inside) |
| Speed/complexity | fastest, dumb | smarter, parses every request |
| Examples | NLB, HAProxy-tcp, kube-proxy | ALB, nginx, Envoy, Traefik |

## 2. Algorithms (token line at the counter)

| Algorithm | Story | Use |
|---|---|---|
| Round robin | token 1→A, 2→B, 3→C… | equal boxes |
| Weighted RR | A gets 3 tokens per round (bigger box) | mixed sizes; drain a node (weight 0!) |
| Least connections | join shortest queue | long-lived (WS, LLM streams!) |
| IP/consistent hash | same street → same counter | caches, sticky-less affinity; consistent ring minimizes reshuffle on scale |
| Least time (EWMA) | fastest hands win | latency-sensitive APIs |

## 3. Health + stickiness + TLS (the fine print)

- **Health checks**: L4 (TCP connect) vs L7 (`GET /ready` → 200 + <300ms). Unhealthy ×N → out of rotation; flap guard (rise/fall counts). **Probes must be cheap** (no full DB scan — see topic 03 ready!).
- **Sticky sessions**: cookie (`AWSALB` / `sessionAffinity: ClientIP`) pins user→pod. Needed for: in-memory carts, WS rooms. Prefer stateless + shared Redis instead (sticky breaks even scaling!).
- **SSL termination/offloading**: LB holds cert, decrypts, inspects/routes, re-encrypts (or plain inside locked VPC). Frees app CPUs (~10× handshake cost) + single cert to rotate.

## 4. CDN = photocopy shops in every city (Cloudflare/CloudFront)

Static (`/static/app.v42.js`, images, video chunks) cached at EDGE near users (20ms vs 300ms). Dynamic API: short-TTL or `stale-while-revalidate` (instant stale + background refresh — topic 02!). **Invalidation**: versioned filenames (deploy-safe forever) > purge API (`/*` purge = thundering herd + bill!). Signed URLs/cookies for private videos (expiry + IP bind).

One-liner: **"L4 routes packets, L7 reads menus; least-conn for streams, hash for caches; health cheap, sticky last-resort; CDN copies static to the edge, version to invalidate."**
Runnable pickers + sticky + health filter: `../examples/05_load_balancer.py`.
