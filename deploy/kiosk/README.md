# Raspberry Pi Kiosk Mode

This folder documents the intended kiosk path. The host API and dashboard should work before kiosk automation is enabled.

## Manual kiosk launch

Start the API:

```bash
source /opt/ai-desk-meter/.venv/bin/activate
ai-meter serve --host 127.0.0.1 --port 8787
```

Open the dashboard in Chromium:

```bash
chromium-browser --kiosk file:///opt/ai-desk-meter/docs/index.html
```

Set the dashboard API URL to:

```text
http://127.0.0.1:8787
```

## Notes

- The Pi runs the host/backend bridge.
- ESP32/Arduino-class boards are companion displays, not the backend authority.
- Keep API binding local unless a trusted LAN display requires access.
