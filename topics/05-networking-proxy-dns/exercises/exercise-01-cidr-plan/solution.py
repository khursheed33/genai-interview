"""Solution: ipaddress does the math; we just ask nicely."""

import ipaddress
import math


def usable(cidr):
    return ipaddress.ip_network(cidr).num_addresses - 2


def contains(cidr, ip):
    return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr)


def carve(cidr, tiers):
    net = ipaddress.ip_network(cidr)
    bits = math.ceil(math.log2(len(tiers)))
    parts = list(net.subnets(prefixlen_diff=bits))
    return dict(zip(tiers, [str(p) for p in parts], strict=True))
