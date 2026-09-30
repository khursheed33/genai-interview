# 07 — Debugging Playbook: Doctor's Bag (symptom → tool)

Don't run tools randomly — match the symptom. Order below = cheap first.

| # | Symptom | Tool | What it proves |
|---|---|---|---|
| 1 | "Is it up?" | `ping` (ICMP echo) | L3 reachability. Blocked ICMP ≠ down (many clouds drop ping!) |
| 2 | "Where does it die?" | `traceroute` / `mtr` (Win: `tracert`) | hop-by-hop latency; `* * *` = filtered hop, sudden jump = guilty link |
| 3 | "Wrong IP?" | `nslookup` (quick) / `dig +trace` (full walk) / `dig @8.8.8.8` (bypass cache) | DNS truth vs cache vs hosts-file lie |
| 4 | "App or net?" | `curl -v` (TLS+headers!), `-w "%{time_connect} %{time_appconnect} %{time_total}"` (DNS vs TLS vs TTFB split!) | slow DNS vs slow TLS vs slow app |
| 5 | "Who listens?" | `ss -tlnp` / `netstat -ano` | port bound? `0.0.0.0` vs `127.0.0.1`? TIME_WAIT flood? |
| 6 | "Talk raw?" | `telnet host 443` / `nc -vz host port` | TCP open without app logic (is the firewall eating it?) |
| 7 | "Cert drama?" | `openssl s_client -connect api:443 -servername api` | chain OK? expiry? SNI mismatch? (`-servername` matters behind CDNs!) |
| 8 | "Packet truth?" | `tcpdump -i any port 443` / Wireshark | retransmits? RST? TLS alert? (decrypt with keylog in dev only!) |

## Corporate classics (interview favorites!)

- `pip install` hangs in office → `HTTPS_PROXY` set but `NO_PROXY` missing `pypi.org`? proxy needs auth? (`curl -x $HTTPS_PROXY https://pypi.org` isolates it).
- `SSL: CERTIFICATE_VERIFY_FAILED` in office → TLS-intercepting proxy! Trust its CA (`REQUESTS_CA_BUNDLE`/`NODE_EXTRA_CA_CERTS`) or escalate — NEVER `verify=False` in prod code.
- Works on WiFi, fails on VPN → split-tunnel/DNS: VPN DNS answers private IP your WiFi can't route; check `nslookup` on each network + `ip route`.
- `curl` works, browser fails → CORS/proxy PAC (browser-only rules!); browser works, `curl` fails → missing headers/cookies the browser auto-sends.

One-liner: **"ping→trace→dig→curl-timings→ss→telnet→openssl→tcpdump: cheap first, and always split DNS vs TLS vs app time."**
Runnable offline-safe probes (localhost): `../examples/07_debug_probes.py`.
