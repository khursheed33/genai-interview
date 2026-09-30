# 02 — Addresses, Subnets, NAT & the Private Cloud (VPC)

## 1. IP + CIDR (street + house range in one line)

- IPv4 `10.0.3.27` (32-bit, ~4B — exhausted → NAT + IPv6 `2001:db8::1`, 128-bit).
- **CIDR** `10.0.0.0/16` = first 16 bits fixed (network), rest hosts: `2^(32-16) - 2 = 65,534` usable (minus network+broadcast).
- Private ranges (never on internet): `10/8`, `172.16/12`, `192.168/16`. If prod shows these to users — something leaks internal topology.

```python
import ipaddress

net = ipaddress.ip_network("10.0.1.0/24")
net.num_addresses  # 256 (254 usable)
"10.0.1.77" in net  # True — is this IP in my subnet?
list(net.subnets(prefixlen_diff=2))  # split /24 into four /26 (db/app/cache/mgmt!)
```

## 2. Subnets + routing (society sectors + watchman diary)

- Split VPC `10.0.0.0/16` → **public** `10.0.1.0/24` (ALB, NAT GW) + **private** `10.0.11.0/24` (app), `10.0.21.0/24` (DB — no internet route at all!).
- **Route table** per subnet: `0.0.0.0/0 → IGW` (public) vs `0.0.0.0/0 → NAT-GW` (private out-only) vs DB (local only).
- **NAT**: 50 private laptops share 1 public IP — gateway rewrites `10.0.3.9:51234 → 203.0.113.7:62001` and remembers the mapping (see `../examples/02_cidr_subnets.py` table demo). Inbound unsolicited? Dropped (that's why private DBs are safe-ish).

## 3. VPC armor (AWS words, all clouds rhyme)

| Layer | Stateful? | Story |
|---|---|---|
| **Security Group** (instance/ENI) | ✅ remembers return traffic | flatmates' pact: "allow 443 from ALB, 5432 from app-SG" (reference SGs, not IPs!) |
| **NACL** (subnet) | ❌ each direction listed | society gate register: allow ephemeral 1024–65535 BOTH ways or return packets die |
| Firewall/WAF | L3–L7 | edge bouncer (DDoS + OWASP rules — topic 04) |

- **Bastion/jump host**: ONE hardened SSH door into private subnets (or better: SSM Session Manager — no inbound 22 at all!). Keys rotated, MFA, session logged.
- **VPN**: encrypted tunnel office↔VPC (Site-to-Site) or laptop↔VPC (Client VPN, WireGuard) — private IPs reachable like LAN. Zero-trust note: VPN ≠ trust (still mTLS + auth per service!).

One-liner: **"Public subnets host doors (ALB/NAT), private host brains, DB darker still; SGs stateful pacts, NACLs dumb lists; reach private via bastion/SSM/VPN."**
