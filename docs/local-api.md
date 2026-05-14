# Local API Bridge

AI Desk Meter includes a small local HTTP API for desktop browsers, Raspberry Pi kiosks, and local dashboard shells.

Start it from the host package:

```bash
cd host
ai-meter serve --host 127.0.0.1 --port 8787
```

Endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Confirms the API process is alive. |
| `GET /providers` | Lists available providers. |
| `GET /status?provider=mock` | Returns one validated dashboard payload. |
| `GET /diagnostics?provider=mock` | Returns a safe diagnostics payload. |

The API is intentionally local-first. It should normally bind to `127.0.0.1` on desktops. For Raspberry Pi kiosk use, bind to a LAN interface only on trusted networks.

The API does not require Arc-RAR to be installed. If `arcrar-cli` is selected and the backend is missing, it returns a clean offline payload rather than crashing.
