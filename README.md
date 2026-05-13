# AI Desk Meter

**AI Desk Meter** is a local-first physical desktop usage dashboard for AI coding tools. The first target is a small ESP32-S3 AMOLED display that shows current usage, weekly usage, reset timers, burn-rate warnings, and connection status.

This repo is designed as a full DIY starter package: firmware scaffold, Python host daemon, JSON protocol, docs, examples, enclosure notes, and a polished HTML spec guide.

> This project is for visibility and diagnostics only. It does **not** bypass usage limits, automate quota evasion, rotate accounts, or scrape private dashboards.

## What it builds

A tiny desk display that can show:

- Current usage percentage
- Weekly usage percentage
- Reset countdowns
- Burn-rate state: idle, low, normal, high, critical
- Data confidence: exact, estimated, mock, or unknown
- Offline/stale/error state
- Optional pixel mascot / status animation

## Recommended hardware

Best first target:

- Waveshare **ESP32-S3-Touch-AMOLED-2.16** or similar ESP32-S3 AMOLED board
- USB-C power
- Optional 3D printed enclosure

Cheap prototype:

- Any ESP32-S3 board with a small display supported by Arduino/LovyanGFX/TFT_eSPI

## Architecture

```text
AI tool / local logs / mock provider
        ↓
Python host daemon
        ↓
Normalized JSON payload
        ↓
Wi-Fi POST or BLE characteristic
        ↓
ESP32-S3 display firmware
```

The host computer does the usage collection and estimation. The ESP32 only receives a simple JSON state and renders it.

## Quick start: host mock mode

```bash
cd host
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ai-meter test-payload
ai-meter start --provider mock --transport stdout
```

Send mock data to a Wi-Fi device:

```bash
ai-meter start --provider mock --transport wifi --url http://192.168.1.44/api/state
```

## Firmware quick start

```bash
cd firmware
pio run
pio upload
pio device monitor
```

The firmware scaffold is intentionally board-adaptation friendly. Start from your board vendor's display example, then wire the JSON state parser and renderer into the provided module layout.

## Payload example

```json
{
  "schema": "ai-desk-meter.v1",
  "service": "claude-code",
  "current_percent": 50,
  "weekly_percent": 11,
  "current_reset_seconds": 4920,
  "weekly_reset_seconds": 547200,
  "burn_rate": "normal",
  "status": "Musing...",
  "mode": "active",
  "updated_at": 1760000000,
  "source": "mock",
  "confidence": "mock"
}
```

## Repo layout

```text
ai-desk-meter/
├─ README.md
├─ DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html
├─ docs/
├─ firmware/
├─ host/
├─ examples/
├─ enclosure/
├─ media/
└─ .github/
```

## Roadmap

- **v0.1** Mock meter: static UI + Wi-Fi JSON
- **v0.2** Python host daemon: mock/manual providers, logs, validation
- **v0.3** Real provider adapters where official/local signals exist
- **v0.4** BLE pairing + OTA update path
- **v1.0** Multi-AI desk meter: Claude Code, Codex, Gemini CLI, Ollama/local LLMs

## License

MIT. See `LICENSE`.
