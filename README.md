# AI Desk Meter

🌐 **Live Project Page:** https://garebear99.github.io/ai-desk-meter/

**AI Desk Meter** is a local-first usage, session, and backend-health dashboard for AI coding workflows. The project starts with a lightweight Python host daemon and ESP32/desktop display payloads, then grows into an ARC-compatible control surface where Arc-RAR can provide portable receipts, archive state, diagnostics, and system-hardwire evidence.

The project is designed to remain honest and portable: the dashboard visualizes state reported by providers; it does not invent usage numbers, bypass limits, rotate accounts, scrape private dashboards, or claim exact usage where only estimates are available.

The open-source track keeps the hardware, provider, dashboard, and local API groundwork public. The planned **MuseMeter 3.0** track is the later commercial full package: a second-brain / Neural Synth / AI buddy product built on the stable open foundation. The current `Musing...` state is intentional and means the agent is responding to prompt input or an action is loading.

## Current scope

AI Desk Meter currently provides:

- A Python host daemon with mock/manual provider support
- A conservative Arc-RAR state-file provider for backend integration testing
- A timeout-safe Arc-RAR CLI provider for the next backend boundary
- A local HTTP API bridge for live dashboard refresh
- A diagnostics ZIP exporter that avoids secrets and private prompt/session content
- A JSON payload protocol suitable for dashboards and small hardware displays
- Wi-Fi/stdout transport scaffolds
- Raspberry Pi / Linux SBC install, smoke-test, systemd, and kiosk deployment docs
- ESP32-S3 firmware scaffold for a physical desk meter
- Public docs for hardware, firmware, host app, provider contracts, roadmap, testing, companion devices, licensing direction, and the pixel buddy character
- Example payloads for normal, warning, offline, corrupt, and Arc-RAR-linked states

The original desk-meter feature set is still preserved as the baseline display target:

- Current usage percentage
- Weekly usage percentage
- Reset countdowns
- Burn-rate state: idle, low, normal, high, critical
- Data confidence: exact, estimated, mock, or unknown
- Offline, stale, warning, and error states
- Pixel buddy / status animation with the baseline `✶ Musing...` state
- Local visibility and diagnostics for AI coding tools without bypassing usage limits

## Hardware direction

AI Desk Meter is designed to scale across several device classes:

| Device class | Intended role | Status |
|---|---|---:|
| Desktop/laptop | Full host daemon, dashboard, provider adapters | Primary target |
| Raspberry Pi / Linux SBC | Full host daemon, local dashboard, bridge node, kiosk display | Supported target path |
| ESP32-S3 | Wi-Fi/BLE display endpoint for simple meter payloads | Firmware scaffold included |
| Arduino-class microcontrollers | Companion telemetry/display nodes using simplified serial or compact payload bridges | Roadmap target |

Best first physical target:

- Waveshare **ESP32-S3-Touch-AMOLED-2.16** or similar ESP32-S3 AMOLED board
- USB-C power
- Optional 3D printed enclosure

Cheap prototype target:

- Any ESP32-S3 board with a small display supported by Arduino, LovyanGFX, or TFT_eSPI

Raspberry Pi-class systems can run the Python host and dashboard stack directly. Arduino-class systems should be treated as endpoints or companion nodes, not as the full backend authority.

## Architecture

```text
AI workflow / local logs / Arc-RAR state / manual input
        ↓
Provider layer
        ↓
Validated AI Desk Meter payload
        ↓
Transport layer: stdout / Wi-Fi / future BLE / future serial
        ↓
Dashboard, Raspberry Pi kiosk, ESP32 display, or companion microcontroller
```

Backend truth belongs to the provider/backend layer. The dashboard and display layers only render validated payloads and error states.

## Quick start: host mock mode

```bash
cd host
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ai-meter test-payload
ai-meter providers
ai-meter start --provider mock --transport stdout --once
```

Send mock data to a Wi-Fi device:

```bash
ai-meter start --provider mock --transport wifi --url http://192.168.1.44/api/state
```

## Arc-RAR state-file provider

The first Arc-RAR bridge intentionally uses a local JSON state file so the dashboard can be tested without binding to unstable internals.

```bash
cd host
AI_METER_ARCRAR_STATE=../examples/arcrar_meter_state.example.json   ai-meter start --provider arcrar --transport stdout --once
```

The future integration target is a stable Arc-RAR CLI/API boundary such as:

```text
arc-rar status --json
arc-rar receipts latest --json
arc-rar archive verify --json
arc-rar session inspect --json
```

AI Desk Meter should consume stable command/API output rather than private Arc-RAR internals.


## Arc-RAR CLI provider

The next backend integration path is now included as `arcrar-cli`. It calls a stable Arc-RAR executable boundary, validates JSON, and fails closed when the executable is missing, times out, exits non-zero, or returns invalid output.

```bash
cd host
ai-meter status --provider arcrar-cli
ai-meter start --provider arcrar-cli --transport stdout --once
```

By default it looks for `arc-rar` on `PATH`. Override the executable and timeout when testing:

```bash
AI_METER_ARCRAR_BIN=/path/to/arc-rar AI_METER_ARCRAR_TIMEOUT=3 ai-meter status --provider arcrar-cli
```

The expected backend command is:

```text
arc-rar status --json
```

The state-file provider remains useful for development and hardware demos; the CLI provider is the preferred path toward live backend authority.


## Local API and live dashboard

AI Desk Meter now includes a local HTTP API bridge so the dashboard can refresh live provider state instead of remaining static.

```bash
cd host
ai-meter serve --host 127.0.0.1 --port 8787
```

Available local endpoints:

```text
GET /health
GET /providers
GET /status?provider=mock
GET /status?provider=arcrar
GET /status?provider=arcrar-cli
GET /diagnostics?provider=mock
```

Open `docs/index.html` or the GitHub Pages dashboard and use the live panel with:

```text
http://127.0.0.1:8787
```

The dashboard fails safely: if the API is offline, Arc-RAR is missing, or a provider returns invalid state, it shows an offline/error payload rather than inventing backend truth.

## Diagnostics export

Create a shareable diagnostics bundle without secrets, tokens, private prompts, or private AI session content:

```bash
cd host
ai-meter diagnostics --provider mock --out ai-desk-meter-diagnostics.zip
ai-meter diagnostics --provider arcrar-cli --out arcrar-diagnostics.zip
```

The ZIP includes `payload.json`, `diagnostics.json`, `provider.txt`, `environment.txt`, `errors.json`, and `README_DIAGNOSTICS.txt`.

## Raspberry Pi / Linux SBC deployment

Install and smoke-test the host stack on Raspberry Pi-class systems or Linux SBCs:

```bash
bash scripts/install_linux_sbc.sh
bash scripts/run_smoke_test.sh
```

A hardened systemd unit and example environment file are included:

```text
deploy/systemd/ai-desk-meter.service
examples/systemd.env.example
```

Read `docs/raspberry-pi-setup.md`, `docs/linux-sbc-validation.md`, and `docs/network-security.md` before binding the API to a LAN address.

## Firmware quick start

```bash
cd firmware
pio run
pio upload
pio device monitor
```

The firmware scaffold is intentionally board-adaptation friendly. Start from your board vendor's display example, then wire the JSON parser and renderer into the provided module layout.

## Payload example

```json
{
  "schema": "ai-desk-meter.v1",
  "service": "arc-rar",
  "current_percent": 12,
  "weekly_percent": 4,
  "current_reset_seconds": 3600,
  "weekly_reset_seconds": 604800,
  "burn_rate": "low",
  "status": "Arc-RAR linked",
  "mode": "active",
  "updated_at": 1760000000,
  "source": "arcrar",
  "confidence": "estimated",
  "backend": {
    "name": "Arc-RAR",
    "receipt_state": "available",
    "archive_state": "verified",
    "hardwire_state": "portable"
  },
  "warnings": [],
  "errors": []
}
```

## Repo layout

```text
ai-desk-meter/
├─ README.md
├─ DIY_Claude_Code_Desk_Usage_Meter_Spec_Guide.html
├─ docs/
│  ├─ architecture.md
│  ├─ provider-contract.md
│  ├─ arcrar-integration-spec.md
│  ├─ raspberry-pi-setup.md
│  ├─ linux-sbc-validation.md
│  ├─ network-security.md
│  ├─ companion-bridge.md
│  ├─ licensing-roadmap.md
│  ├─ character-spec.md
│  ├─ test-matrix.md
│  └─ neural-synth-roadmap.md
├─ scripts/
├─ deploy/
├─ firmware/
├─ host/
├─ examples/
├─ tests/
└─ enclosure/
```

## Roadmap summary

- **v0.1** Clean dashboard + mock/manual providers
- **v0.2** Arc-RAR state-file provider
- **v0.3** Arc-RAR CLI/API provider ✅
- **v0.4** Live dashboard provider refresh and diagnostics export ✅
- **v0.5** Raspberry Pi / Linux SBC kiosk validation ✅
- **v0.6** ESP32 display endpoint hardening
- **v0.7** Arduino-class companion telemetry bridge design
- **v0.8** Native dashboard shell prototype
- **v1.0** Stable Arc-RAR-backed AI Desk Meter
- **v1.1+** Omnibinary adapter, ARC-Core hardwire integration, archive timeline view, Neural Synth toggle page
- **v3.0** MuseMeter commercial full package: second-brain / Neural Synth / AI buddy product
- **Future provider targets** Multi-AI desk meter support where official/local signals exist: Claude Code/manual logs, Codex-style CLI workflows, Gemini CLI-style workflows, Ollama/local LLMs, and other local-first provider adapters

## Validation

Current package validation:

```text
pytest: 18 passed
mock provider works
state-file Arc-RAR provider works
Arc-RAR CLI provider fails closed for missing executable, invalid JSON, non-zero exit, and timeout
local API bridge works for `/health`, `/providers`, `/status`, and `/diagnostics`
diagnostics ZIP export works without including secrets or private prompt/session content
Linux/SBC install script, smoke-test script, systemd unit, kiosk docs, and network-safety docs are included
```

## License

MIT for the current open-source corridor. See `LICENSE` and `docs/licensing-roadmap.md`. The planned MuseMeter 3.0 package is intended to move to a commercial license after the open foundation is stable.
