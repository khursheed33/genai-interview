# 06 — Tunnels, Discovery & Mesh: Secret Passages & Hotel Directories

## 1. Port forwarding (doors that lead elsewhere)

| Command | Story | Use |
|---|---|---|
| `ssh -L 5433:db.internal:5432 bastion` | local door 5433 → tunnel → private DB | debug prod DB with local GUI (close when done!) |
| `ssh -R 8080:localhost:3000 bastion` | bastion's 8080 → YOUR laptop | demo local build to a teammate; webhook testing |
| `ssh -D 1080 bastion` (SOCKS) | browser wears bastion's shoes | browse private dashboards as if inside VPC |
| `kubectl port-forward svc/api 8000:80` | k8s-flavored `-L` | same idea, no SSH |

Rules: `-N` (no shell, forward only) + `-f` (background) + key auth; REVERSE forwards are powerful = restrict in `sshd_config` (`AllowTcpForwarding remote` + `PermitOpen`). Never `-R` to share secrets publicly!

## 2. Service discovery (hotel directory that updates itself)

Hardcoded `10.0.11.9` dies on redeploy. Instead: **DNS** (`api.svc.cluster.local` → current pods, CoreDNS!), **registry** (Consul/etcd: services register + health-check, clients watch), **K8s Services** (virtual IP + kube-proxy L4 balance). Client-side (gRPC pick-first/round-robin) vs server-side (ALB/Envoy) — same algorithms as note 05, new address book.

## 3. Service mesh (Istio/Linkerd): receptionists in EVERY doorway

Sidecar proxy next to EACH pod: all traffic in/out passes Envoy → uniform mTLS (identity per workload, auto-rotated via SDS!), retries/timeouts, telemetry, traffic splits (canary 5%→new), policy (this SA may call payments — else 403).

- Istio (rich, heavier) vs Linkerd (tiny, Rust sidecar). Cost: +latency (~ms) + CPU + operational brain. Worth it at 20+ services with compliance needs; YAGNI at 3 services (a gateway + libs do fine).
- Mesh mTLS ≠ topic-04 app mTLS knowledge wasted — same certs, now automatic: workloads get SPIFFE IDs (`spiffe://shop/payments`), rotation without restarts.

One-liner: **"Forward (`-L`) to reach in, reverse (`-R`) to show out, SOCKS (`-D`) to browse as insider; discover via DNS/registry, mesh when dozens of services need uniform mTLS+policy."**
Command builder (validated flags!): `../examples/06_tunnel_cmds.py`.
