"""01_tcp_udp_sockets.py — phone call vs postcard, for real on localhost.

Run: uv run python topics/05-networking-proxy-dns/examples/01_tcp_udp_sockets.py
"""

import socket
import threading

# --- TCP echo: handshake + ordered reliable stream (phone call) ---
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 0))
srv.listen(1)
port = srv.getsockname()[1]


def serve_once():
    conn, _addr = srv.accept()  # blocks till SYN-SYN/ACK-ACK done by OS
    with conn:
        data = conn.recv(1024)
        conn.sendall(b"echo:" + data)


threading.Thread(target=serve_once, daemon=True).start()
c = socket.create_connection(("127.0.0.1", port), timeout=5)  # handshake here
c.sendall(b"dosa")
assert c.recv(1024) == b"echo:dosa"
c.close()
srv.close()
print(f"TCP: handshake + echo ok on 127.0.0.1:{port} (ESTABLISHED then closed)")


# --- UDP: fire-and-forget postcards ---
u_srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
u_srv.bind(("127.0.0.1", 0))
u_port = u_srv.getsockname()[1]
u_cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
u_cli.sendto(b"ping-postcard", ("127.0.0.1", u_port))
u_srv.settimeout(5)
data, _ = u_srv.recvfrom(1024)
assert data == b"ping-postcard"
print("UDP: postcard sent + received, no handshake, no guarantees")


def port_open(host, p, timeout=1.0):
    try:
        socket.create_connection((host, p), timeout=timeout).close()
        return True
    except OSError:
        return False


assert port_open("127.0.0.1", u_port) is False  # UDP port invisible to TCP probe!
print(
    "OK — TCP = seq/ack reliability; UDP = 1 packet; probe with TCP connect (ss -tlnp shows LISTEN)"
)
