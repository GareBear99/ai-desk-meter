# Raspberry Pi / Linux SBC Setup

AI Desk Meter can run as a full local host/dashboard stack on Raspberry Pi-class systems and other Linux SBCs. The recommended path is Raspberry Pi OS Lite or Desktop, Python 3.10+, and a local browser or kiosk session.

## Supported role

A Raspberry Pi can run:

- the Python host package
- the local HTTP API
- mock/manual providers
- Arc-RAR state-file provider
- Arc-RAR CLI provider when Arc-RAR is installed for that system
- diagnostics export
- local browser/kiosk dashboard

Arduino-class boards should not run the full host stack. They should act as display or telemetry companion endpoints.

## Install

```bash
bash scripts/install_linux_sbc.sh
source .venv/bin/activate
ai-meter providers
ai-meter status --provider mock
```

## Run local API

```bash
ai-meter serve --host 127.0.0.1 --port 8787
```

Open the dashboard locally and point it at:

```text
http://127.0.0.1:8787
```

## Smoke test

```bash
bash scripts/run_smoke_test.sh
```

The smoke test checks provider registration, mock payload JSON, diagnostics export, API boot, `/health`, and `/status`.

## systemd install outline

For a production-ish Pi install, copy the repo to `/opt/ai-desk-meter`, install the virtual environment there, create an `ai-meter` user, copy the systemd unit, and enable it.

```bash
sudo useradd --system --home /var/lib/ai-desk-meter --shell /usr/sbin/nologin ai-meter || true
sudo mkdir -p /opt/ai-desk-meter /var/lib/ai-desk-meter /var/log/ai-desk-meter
sudo chown -R ai-meter:ai-meter /var/lib/ai-desk-meter /var/log/ai-desk-meter
sudo cp examples/systemd.env.example /etc/ai-desk-meter.env
sudo cp deploy/systemd/ai-desk-meter.service /etc/systemd/system/ai-desk-meter.service
sudo systemctl daemon-reload
sudo systemctl enable --now ai-desk-meter
sudo systemctl status ai-desk-meter
```

Default binding is `127.0.0.1`. Only bind to LAN after reading `docs/network-security.md`.
