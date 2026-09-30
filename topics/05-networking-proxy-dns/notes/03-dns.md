# 03 — DNS: Internet Phonebook (records → resolution → custom domains)

## 1. Records (the 9 that pay rent)

| Type | Story | Example |
|---|---|---|
| A / AAAA | name → IPv4 / IPv6 | `api.shop.com → 203.0.113.7` / `→ 2001:db8::7` |
| CNAME | nickname → real name (no other records alongside!) | `www → shop.com` (apex/naked domain CAN'T be CNAME → use ALIAS/ANAME) |
| MX | post office for mail (+ priority) | `10 mail.shop.com` |
| TXT | sticky notes (SPF/DKIM/verification) | `"v=spf1 include:_spf.google.com ~all"` |
| NS | who answers for this zone | `ns1.cloudflare.com` |
| SRV | service+port+weight (`_xmpp._tcp`) | chat/voice discovery |
| PTR | reverse: IP → name (mail trust!) | `7.113.0.203.in-addr.arpa → mail.shop.com` |
| SOA | zone's birth certificate (serial/refresh) | bump serial or secondaries ignore you |

- **TTL** (seconds): "remember this answer this long". 300 = agile (migration day!), 86400 = calm. Lower BEFORE migrations (a day ahead!), raise after.

## 2. Resolution walk (recursive vs authoritative)

```
you → [recursive: ISP/1.1.1.8] → root (".") → TLD ("com") → authoritative ("shop.com")
         ↑ caches every step (TTL!)                    ↑ OWNS the truth (Route53/Cloudflare)
```

- `dig +trace api.shop.com` shows the walk; plain `dig` hits cache. **Caching layers**: browser → OS → recursive — stale record? `TTL` wait or flush; negative answers cache too (typo'd domain "doesn't exist" for 5 min!).
- **Split-horizon**: same name, different answers — office WiFi gets `10.0.5.9` (private API), internet gets `203.0.113.7`. Route53 views / CoreDNS rewrites do this.

## 3. Local mapping ladder (dev → prod)

`hosts file` (`127.0.0.1 myapp.local`) → `dnsmasq` (team wildcard `*.test → 127.0.0.1`) → `CoreDNS` (K8s `svc.cluster.local`!) → `Route53/Cloudflare` (prod). Debugging order in `07-debugging.md`: hosts-file typo has burned every engineer once.

## 4. Custom domain setup (the ritual, in order)

1. Buy/verify domain → 2. `A/ALIAS → ALB IP` + `CNAME www → apex` (+ wildcard `*.shop.com` for tenants) → 3. provision cert (ACM/Let's Encrypt — HTTP/DNS-01 challenge) → 4. bind cert to ALB/ingress + force HTTPS (301 + HSTS) → 5. lower TTL a day before cutover, watch propagation (`dig @8.8.8.8` vs `@1.1.1.1`).

One-liner: **"A=address, CNAME=nickname (never apex), MX=mail, TXT=proofs; TTL low before moves; split-horizon inside, public outside."**
Runnable: packet builder + TTL cache in `../examples/03_dns_cache.py`.
