# Interview Questions — Networking, Proxy & DNS

Say the **bold line** first, then the hook.

## TCP/IP & addressing

- [ ] **[theory]** TCP vs UDP + 3-way handshake in 60 seconds?
  - **TCP = phone call (seq/ack, ordered, retransmit); UDP = postcard (fast, lossy). Handshake: SYN → SYN-ACK → ACK; SYN floods → SYN cookies + edge absorb.**
- [ ] **[hands-on]** Private ranges? `/20` usable hosts? Is `10.5.9.9` in `10.5.0.0/16`?
  - **`10/8, 172.16/12, 192.168/16`. `2^(32-20)-2 = 4094`. `ipaddress` module answers membership in one line.**
- [ ] **[theory]** NAT outbound vs inbound? Public vs private subnets?
  - **Outbound rewrites+remembers (many→one IP); unsolicited inbound dropped. Public hosts doors (ALB/NAT), private hosts brains, DB no-internet-route.**
- [ ] **[theory]** SG vs NACL vs bastion vs VPN?
  - **SG stateful per-instance pacts (reference SGs!); NACL stateless subnet lists (allow ephemeral both ways); bastion/SSM single SSH door; VPN extends LAN (still zero-trust inside!).**

## DNS

- [ ] **[hands-on]** A vs CNAME vs MX vs TXT vs PTR? Apex CNAME?
  - **A/AAAA = address; CNAME = nickname (never at apex — use ALIAS); MX = mail; TXT = proofs (SPF/DKIM); PTR = reverse (mail trust).**
- [ ] **[theory]** Recursive vs authoritative? `dig` vs `dig +trace`? TTL before migration?
  - **Recursive caches (ISP/1.1.1.1), authoritative owns truth. Plain dig = cache; +trace = full walk. Lower TTL a day BEFORE moves.**
- [ ] **[scenario]** Same name, office gets `10.x`, internet gets `203.x` — what + how?
  - **Split-horizon DNS (Route53 views/CoreDNS rewrites). Debug: compare `dig @8.8.8.8` vs office resolver + check hosts file first!**
- [ ] **[hands-on]** Custom domain ritual for a new API?
  - **A/ALIAS + `CNAME www` (+ wildcard) → cert via ACM/LE → bind to ALB/ingress → 301+HSTS → watch propagation on two resolvers.**

## Proxies & LB & CDN

- [ ] **[theory]** Forward vs reverse vs transparent — draw + one use each?
  - **Forward hides clients (corp egress + `NO_PROXY` for internal!). Reverse hides servers (TLS/LB/cache at one door). Transparent = invisible tap.**
- [ ] **[hands-on]** nginx: `location` order? `proxy_pass` slash lore? 3 headers you must set?
  - **`=` > `^~` > `~` regex > prefix. Trailing slash rewrites URI (test it!). Always `Host`, `X-Forwarded-For/Proto`, `X-Request-ID` — and READ XFF leftmost in app.**
- [ ] **[theory]** L4 vs L7? RR vs least-conn vs hash — pick for: equal APIs, WS rooms, cache fleet?
  - **L4 = packets (fast/dumb/NLB); L7 = menus (ALB/nginx, path/header routing, TLS terminate). Equals → RR; streams → least-conn; caches → consistent hash; drain via weight 0.**
- [ ] **[theory]** Health checks cheap? Sticky when? SSL offload why?
  - **`GET /ready` 200 fast (no DB scan!). Sticky = last resort (prefer stateless+Redis). Terminate at LB: one cert, frees app CPUs.**
- [ ] **[theory]** CDN caches what? Invalidate how for private video?
  - **Static at edge (versioned filenames = free invalidation). Private: signed URLs + short TTL; `/*` purge = herd + bill.**

## Tunnels / mesh / debugging

- [ ] **[hands-on]** `-L` vs `-R` vs `-D` vs `kubectl port-forward`?
  - **`-L` reach in (local:5433→private DB), `-R` show out (teammate sees my laptop), `-D` browse as insider (SOCKS), k8s-fwd same without SSH. `-N` no-shell; lock down reverse in sshd.**
- [ ] **[theory]** Discovery via? Mesh buys what, costs what?
  - **DNS (`*.svc.cluster.local`) / Consul / K8s Services. Mesh (Istio/Linkerd sidecars): uniform mTLS+retries+canary splits; costs ms + CPU + brain — YAGNI at 3 services.**
- [ ] **[scenario]** Order: `pip install` hangs in office / `CERTIFICATE_VERIFY_FAILED` / WiFi-ok-VPN-fails / curl-ok-browser-fails?
  - **Proxy env (`NO_PROXY`? auth?) → TLS-intercepting proxy CA (never `verify=False` prod!) → split-tunnel DNS/routes → browser-only CORS/PAC vs missing headers in curl.**
- [ ] **[hands-on]** Split slow request into DNS vs TLS vs app — exact flags?
  - **`curl -w "connect:%{time_connect} tls:%{time_appconnect} total:%{time_total}"`; then `dig`, `openssl s_client -servername`, `ss -tlnp`, `tcpdump` — cheap first.**

## Gotchas (say unprompted)

- `0.0.0.0` vs `127.0.0.1` bind (debug UI on all doors = breach); missing intermediate cert = mobile-only failures.
- No `NO_PROXY` for `.cluster.local` = self-traffic via proxy death; `TIME_WAIT` floods in load tests.
- Wildcard cert ≠ wildcard DNS (`*.shop.com` record still needed); negative DNS answers cache too.

## Self-score (0–5)

- TCP/IP+subnets: __ / DNS: __ / proxies: __ / LB+CDN: __ / tunnels+mesh: __ / debugging: __
- Whiteboard: handshake + split-horizon + nginx block + `-L` command? Y/N each.
