# Deployment

How `football.jaeyeongyun.dev` is actually run in production. This document
(and the config under `deploy/`) mirrors what's live on the EC2 instance —
verified by SSHing in and reading the running config, not written from memory.

## Architecture

```
Internet (443/80)
      │
      ▼
   Nginx  ── reverse proxy, TLS termination, rate limiting on /api/
      │  proxy_pass http://127.0.0.1:8000
      ▼
  Gunicorn (2 workers) ── bound to 127.0.0.1:8000 only, not exposed directly
      │  runs app:app
      ▼
   Flask app (this repo)

Guarded by: ufw (default-deny inbound, only 22/80/443 open) + fail2ban
```

## 1. Service user and app directory

The app does **not** run as `ubuntu` or `root`. A dedicated, unprivileged
user owns the code and the virtualenv:

```bash
sudo useradd --system --create-home --shell /usr/sbin/nologin football
sudo mkdir -p /opt/football
sudo chown football:football /opt/football
```

Deploy the repo into `/opt/football`, then as the `football` user:

```bash
python3 -m venv /opt/football/venv
/opt/football/venv/bin/pip install -r requirements.txt
```

## 2. Gunicorn, managed by systemd

Gunicorn is never started by hand — `systemd` owns the process lifecycle,
including automatic restart on crash and on boot.

Config: [`deploy/systemd/football.service`](deploy/systemd/football.service)

```bash
sudo cp deploy/systemd/football.service /etc/systemd/system/football.service
sudo systemctl daemon-reload
sudo systemctl enable --now football
```

Key choices:
- `--bind 127.0.0.1:8000` — Gunicorn only listens on localhost; it is never
  reachable directly from the internet, only through Nginx.
- `--workers 2` — sized for the instance's vCPU count.
- `Restart=always` / `RestartSec=5` — the worker set comes back on its own
  after a crash or a reboot, without anyone SSHing in.

Verify:
```bash
systemctl status football
```

## 3. Nginx — reverse proxy, TLS, rate limiting

Config: [`deploy/nginx/football.conf`](deploy/nginx/football.conf),
[`deploy/nginx/ratelimit.conf`](deploy/nginx/ratelimit.conf)

```bash
sudo cp deploy/nginx/ratelimit.conf /etc/nginx/conf.d/ratelimit.conf
sudo cp deploy/nginx/football.conf /etc/nginx/sites-available/football
sudo ln -s /etc/nginx/sites-available/football /etc/nginx/sites-enabled/football
sudo nginx -t && sudo systemctl reload nginx
```

- `/api/` is rate-limited to 30 requests/minute per IP
  (`limit_req_zone ... rate=30r/m`, `burst=10 nodelay`) — the `/api/simulate`
  Monte Carlo endpoint is the expensive one to spam, so it gets its own
  limited location block.
- Everything else proxies straight through to Gunicorn on `127.0.0.1:8000`.
- Port 80 is kept open only to redirect to HTTPS and to serve Let's Encrypt's
  ACME challenge; it returns 404 for anything else.

## 4. TLS via Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d football.jaeyeongyun.dev
```

Certbot edits the Nginx server block in place (the `# managed by Certbot`
lines in `deploy/nginx/football.conf` are its doing, left untouched here) and
installs its own renewal timer — no manual cron job needed:

```bash
systemctl list-timers | grep certbot
sudo certbot renew --dry-run   # confirms auto-renewal will actually work
```

## 5. Firewall and brute-force protection

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

sudo apt install fail2ban
sudo systemctl enable --now fail2ban
```

Result: only SSH (22) and HTTP/HTTPS (80/443) are reachable from the
internet; everything else is dropped by default. `fail2ban` watches auth
logs and bans repeat-offender IPs.

## Verifying all of the above on a running box

These are read-only checks — nothing here changes running state:

```bash
systemctl status football
sudo ufw status verbose
sudo systemctl status fail2ban
sudo nginx -T | grep -i ssl_certificate
sudo certbot certificates
```
