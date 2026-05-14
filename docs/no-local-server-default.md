# No Local Server Required

AI Desk Meter is offline-first by default. The normal runtime path does **not** require a local HTTP server.

Default flow:

```text
provider/backend state -> validated JSON payload -> file/stdout/serial/Wi-Fi bridge -> dashboard or device
```

The local HTTP API remains available only for development, browser preview, and LAN debugging. It is not required for MuseMeter, Raspberry Pi kiosk mode, companion hardware, or normal desktop usage.

## Default file payload commands

Write a full dashboard payload once:

```bash
ai-meter write-status --provider mock --out runtime/status.json
```

Write a compact companion payload once:

```bash
ai-meter write-companion --provider mock --out runtime/companion.json
```

Continuously refresh files:

```bash
ai-meter watch --provider mock --out runtime/status.json --interval 2
ai-meter watch-companion --provider mock --out runtime/companion.json --interval 2
```

## Device-friendly outputs

- Full dashboards should read `runtime/status.json`.
- ESP32/Arduino companion displays should read `runtime/companion.json`, serial output, or a compact bridge.
- Tauri/native shells should read local JSON files directly where possible.

## Optional dev server

The server is still useful for quick browser testing:

```bash
ai-meter serve --host 127.0.0.1 --port 8787
```

Treat it as optional preview tooling, not as the product dependency.
