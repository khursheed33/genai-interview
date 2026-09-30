# 04 — Proxies: Secretary vs Receptionist (forward/reverse + nginx)

## 1. The two directions (draw this in interviews!)

```
FORWARD (your secretary):  you → [proxy] → internet   (hides CLIENTS; corp control)
REVERSE (shop reception):  internet → [proxy] → app1/app2 (hides SERVERS; TLS/LB/cache)
TRANSPARENT: same as reverse but client doesn't know (ISP cache, WAF tap)
```

- **Forward**: corp egress control (allowlist github/pypi only!), caching, DLP scan. Config via `HTTP_PROXY/HTTPS_PROXY/NO_PROXY` (+ lowercase twins!) — `NO_PROXY=localhost,127.0.0.1,.cluster.local` or your own services loop through the proxy and die. `PAC` files = per-URL proxy chooser (JS function in browsers). Proxy-AUTH (`Proxy-Authorization: Basic`) breaks CLIs that forget it — pip/npm/docker all need explicit proxy config!
- **Reverse** (nginx/Envoy/Traefik/ALB): ONE public door → TLS termination → routing → 5 private apps. Client never learns `10.0.11.9`.

## 2. nginx in 15 lines (read any config after this)

```nginx
upstream api { server 10.0.11.9:8000 max_fails=3 fail_timeout=30s; server 10.0.11.10:8000; }
server {
  listen 443 ssl; server_name api.shop.com;
  ssl_certificate /etc/ssl/shop.crt; ssl_certificate_key /etc/ssl/shop.key;
  location /v1/ {
    proxy_pass http://api;                       # strip /v1? (trailing-slash lore — test it!)
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;   # real client IP chain!
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Request-ID $request_id;
    proxy_read_timeout 10s;
  }
  location /static/ { alias /var/www/; expires 30d; }  # CDN-origin pattern
  return 301 https://$host$request_uri;          # (in the :80 block) force HTTPS
}
```

- `location` matching: `=` exact > `^~` prefix-no-regex > `~` regex > `/` prefix. `proxy_pass` WITH trailing slash rewrites URI, WITHOUT passes through — #1 nginx bug source. Upstream health: `max_fails/fail_timeout` (passive); Envoy/ALB add ACTIVE checks (topic 05 note).
- App MUST trust proxy headers (`ForwardedIP` middleware reading `X-Forwarded-For` leftmost = real client) AND rate-limit by it (else one IP = whole internet!).

## 3. Apache/Haproxy/Traefik/Envoy one-liners

Apache (`mod_proxy`, `.htaccess` heritage), HAProxy (TCP+HTTP king, `frontend/backend`, stick-tables), Traefik (auto-discovers Docker/K8s labels — zero config), Envoy (xDS API, sidecar of service mesh — topic note 06).

Runnable: live backend + forwarding proxy with header injection in `../examples/04_reverse_proxy.py`.
