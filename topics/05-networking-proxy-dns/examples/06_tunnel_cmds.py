"""06_tunnel_cmds.py — secret passages, validated (never fat-finger a prod forward).

Run: uv run python topics/05-networking-proxy-dns/examples/06_tunnel_cmds.py
"""


def _port(p):
    if not 1 <= int(p) <= 65535:
        raise ValueError(f"bad port {p}")
    return int(p)


def _host(h):
    if not h or any(c in h for c in " ;|&$`"):
        raise ValueError(f"bad host {h!r}")
    return h


def local(local_port, remote_host, remote_port, via):
    return f"ssh -N -L {_port(local_port)}:{_host(remote_host)}:{_port(remote_port)} {_host(via)}"


def remote(remote_port, local_host, local_port, via):
    return f"ssh -N -R {_port(remote_port)}:{_host(local_host)}:{_port(local_port)} {_host(via)}"


def socks(local_port, via):
    return f"ssh -N -D {_port(local_port)} {_host(via)}"


def k8s_fwd(svc, local_port, svc_port, ns="default"):
    return f"kubectl port-forward svc/{svc} {_port(local_port)}:{_port(svc_port)} -n {ns}"


print("IN :", local(5433, "db.internal", 5432, "bastion"))
print("OUT:", remote(8080, "localhost", 3000, "bastion"))
print("AS :", socks(1080, "bastion"))
print("K8S:", k8s_fwd("api", 8000, 80))
assert "-L 5433:db.internal:5432" in local(5433, "db.internal", 5432, "bastion")
try:
    local(99999, "x", 80, "bastion")
    raise AssertionError("bad port accepted?!")
except ValueError:
    pass
try:
    local(8080, "a; rm -rf /", 80, "bastion")
    raise AssertionError("injection accepted?!")
except ValueError:
    pass
print("OK — -L reach in, -R show out, -D browse as insider; -N no-shell, validate all")
