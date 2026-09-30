"""02_cidr_subnets.py — society sectors + watchman's NAT diary.

Run: uv run python topics/05-networking-proxy-dns/examples/02_cidr_subnets.py
"""

import ipaddress

vpc = ipaddress.ip_network("10.0.0.0/16")
print("VPC usable hosts:", vpc.num_addresses - 2)
assert vpc.num_addresses == 65536

public, private_app, private_db = list(vpc.subnets(new_prefix=18))[:3]
print("public:", public, "| app:", private_app, "| db:", private_db)
assert ipaddress.ip_address("10.0.3.9") in vpc and ipaddress.ip_address("10.0.200.9") in vpc
assert ipaddress.ip_address("11.0.0.1") not in vpc


def split_for_tiers(net, tiers=("public", "app", "db", "mgmt")):
    parts = list(net.subnets(prefixlen_diff=2))  # /24 -> four /26
    return dict(zip(tiers, [str(p) for p in parts], strict=True))


plan = split_for_tiers(ipaddress.ip_network("10.0.1.0/24"))
assert len(plan) == 4 and plan["db"] == "10.0.1.128/26"
print("tier plan:", plan)


class NAT:  # 50 laptops, 1 public IP: rewrite + remember
    def __init__(self, public_ip):
        self.public_ip = public_ip
        self.table, self.next_port = {}, 62000

    def outbound(self, priv_ip, priv_port):
        key = (priv_ip, priv_port)
        if key not in self.table:
            self.next_port += 1
            self.table[key] = self.next_port
        return (self.public_ip, self.table[key])

    def inbound(self, pub_port):
        for (ip, port), mapped in self.table.items():
            if mapped == pub_port:
                return (ip, port)
        return None  # unsolicited inbound? dropped!


nat = NAT("203.0.113.7")
ext = nat.outbound("10.0.3.9", 51234)
assert ext[0] == "203.0.113.7" and nat.inbound(ext[1]) == ("10.0.3.9", 51234)
assert nat.inbound(9999) is None
print("NAT:", ("10.0.3.9", 51234), "->", ext, "| stranger knocking: dropped")
print("OK — CIDR math via ipaddress; NAT rewrites outbound, drops unsolicited inbound")
