"""Solution: validated passages + cheap-first doctor."""

TOOLS = {
    "down?": "ping",
    "where-die": "traceroute",
    "wrong-ip": "dig +trace",
    "app-or-net": "curl -v + timings",
    "who-listens": "ss -tlnp",
    "raw-talk": "telnet/nc",
    "cert": "openssl s_client",
    "packets": "tcpdump",
}


def _port(p):
    if not 1 <= int(p) <= 65535:
        raise ValueError(f"bad port {p}")
    return int(p)


def _host(h):
    if not h or any(c in h for c in " ;|&$`"):
        raise ValueError(f"bad host {h!r}")
    return h


def tunnel(kind, **kw):
    if kind == "local":
        fwd = f"{_port(kw['lport'])}:{_host(kw['rhost'])}:{_port(kw['rport'])}"
        return f"ssh -N -L {fwd} {_host(kw['via'])}"
    if kind == "remote":
        rev = f"{_port(kw['rport'])}:{_host(kw['lhost'])}:{_port(kw['lport'])}"
        return f"ssh -N -R {rev} {_host(kw['via'])}"
    if kind == "socks":
        return f"ssh -N -D {_port(kw['lport'])} {_host(kw['via'])}"
    raise ValueError(f"unknown kind {kind}")


def diagnose(symptom):
    return TOOLS.get(symptom, "start with ping (cheap first)")
