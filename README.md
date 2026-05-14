# AI Desk Meter

🌐 **Live Project Page:** https://garebear99.github.io/ai-desk-meter/

**AI Desk Meter** is a local-first usage, session, and backend-health dashboard for AI coding workflows. The project starts with a lightweight Python host daemon and ESP32/desktop display payloads, then grows into an ARC-compatible control surface where Arc-RAR can provide portable receipts, archive state, diagnostics, and system-hardwire evidence.

The project is designed to remain honest and portable: the dashboard visualizes state reported by providers; it does not invent usage numbers, bypass limits, rotate accounts, scrape private dashboards, or claim exact usage where only estimates are available.

The open-source track keeps the hardware, provider, dashboard, and local API groundwork public. The planned **MuseMeter 3.0** track is the later commercial full package: a second-brain / Neural Synth / AI buddy product built on the stable open foundation. The current `Musing...` state is intentional and means the agent is responding to prompt input or an action is loading.

## Native app holster

Use the packaged GUI holster with one command:

```bash
ai-meter app
```

The native holster and browser preview now share one unified runtime page. The same page includes Muse status, runtime connection state, Dev JSON, internal CLI commands, provider/Omnibinary boundaries, logs, and an integrated Docs / Runtime Info panel. The runtime page includes Muse status, runtime connection state, Dev JSON, internal CLI commands, provider/Omnibinary boundaries, logs, and docs/runtime information. The Dashboard button opens the live runtime dashboard IP page, while Docs opens the docs page/site.

This starts the no-server runtime writer and opens the desktop GUI shell. For headless/no-GUI operation:

```bash
ai-meter runtime --provider mock --out runtime/status.json --interval 0.5
```

`native/launcher` is the practical cross-system native shell path. `native/tauri` remains available for modern Tauri development, and `ai-meter gui` remains a compatibility alias.

## One-command launch

```bash
ai-meter gui
```

This opens the no-server GUI and automatically starts the local runtime writer. For headless/no-GUI use:

```bash
ai-meter runtime --provider mock --out runtime/status.json --interval 0.5
```

## Current scope

**Current release:** v1.0.7 — stable open-source functional foundation with native SVG eye blink control, exact `No Muse.` SVG disconnected label, `No active Muse` connection state, and faster no-server runtime refresh.


AI Desk Meter currently provides:

- A Python host daemon with mock/manual provider support
- A conservative Arc-RAR state-file provider for backend integration testing
- A timeout-safe Arc-RAR CLI provider with status, receipt, archive, and session contract fixtures
- Offline-first JSON file/stdout flows for dashboards and companion devices
- An optional local HTTP API bridge for development/debug live dashboard refresh
- A diagnostics ZIP exporter that avoids secrets and private prompt/session content
- A local `doctor` command for functional health checks
- A JSON payload protocol suitable for dashboards and small hardware displays
- Wi-Fi/stdout transport scaffolds
- Raspberry Pi / Linux SBC install, smoke-test, systemd, and kiosk deployment docs
- ESP32-S3 firmware scaffold for a physical desk meter
- Compact companion JSON payloads for ESP32 and Arduino-class companion displays
- Optional `/companion/status` endpoint for development/debug previews
- Real Tauri/Rust native desktop shell under `native/tauri` that reads `runtime/status.json` with no local server required
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

## Release and license path

- `v1.0.3` adds the real Tauri/Rust native desktop shell while preserving no-server defaults.
- `v1.0.7` makes the actual SVG buddy label say `No Muse.` when no active Muse/model payload is connected, while preserving the main `No active Muse` header and active `✶ Musing...` state.
- `v1.0.6` removes overlay blink elements, hooks blink behavior directly into the two SVG eye pixels, preserves `No active Muse`, and reduces no-server refresh increments.
- `v1.0.4` adds explicit `No active Muse` behavior when no valid runtime payload is connected.
- `v1.0.1` is the stable open-source functional release with no local server required by default.
- `v1.0.0` remains the first stable functional release baseline.
- `v1.x-v2.x` remain the open-source foundation/expansion corridor unless a future notice says otherwise.
- `MuseMeter 3.0` is the planned commercial full package: second-brain / Neural Synth / AI buddy.

See `docs/release-v1.0.0.md`, `docs/open-source-boundary.md`, and `docs/version-license-matrix.md`.


## Native desktop app

AI Desk Meter includes a real Tauri/Rust native app under `native/tauri`. It reads `runtime/status.json` directly and does **not** require the optional localhost API.

```bash
# terminal 1
source host/.venv/bin/activate
ai-meter watch --provider mock --out runtime/status.json --interval 0.5

# terminal 2
cd native/tauri
npm install
npm run tauri:dev
```

Build a desktop bundle with:

```bash
cd native/tauri
npm run tauri:build
```

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
ai-meter version
ai-meter providers
ai-meter doctor --provider mock
ai-meter test-payload
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


## Native dashboard shell path

v0.8 adds a desktop-shell path for the existing local API and dashboard. This is a Tauri-oriented prototype scaffold, not a signed desktop release yet.

```bash
./scripts/launch_local_dashboard.sh
# Windows PowerShell:
# ./scripts/launch_local_dashboard.ps1
```

The shell plan keeps the GUI as a viewer/control surface. Provider truth remains in the local host service and backend integrations.

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


## Default runtime: no local server required

AI Desk Meter is offline-first by default. The normal runtime writes validated JSON payloads to files, stdout, serial/Wi-Fi bridges, or companion devices. The local HTTP API is optional development/debug tooling only.

Write one full dashboard payload:

```bash
cd host
ai-meter write-status --provider mock --out ../runtime/status.json
```

Write one compact companion payload:

```bash
ai-meter write-companion --provider mock --out ../runtime/companion.json
```

Continuously refresh file payloads:

```bash
ai-meter watch --provider mock --out ../runtime/status.json --interval 0.5
ai-meter watch-companion --provider mock --out ../runtime/companion.json --interval 0.5
```

Open `docs/index.html` directly and use the file-import control to load `runtime/status.json`. Native/Tauri shells and Raspberry Pi kiosk setups should prefer file/stdout/serial flows over a required server.

## Optional local API and live dashboard preview

The local HTTP API is still included for development, browser preview, and LAN/debug testing. It is not required for normal use.

```bash
cd host
ai-meter serve --host 127.0.0.1 --port 8787
```

Available optional endpoints:

```text
GET /health
GET /providers
GET /status?provider=mock
GET /status?provider=arcrar
GET /status?provider=arcrar-cli
GET /companion/status?provider=mock
GET /diagnostics?provider=mock
```

The dashboard fails safely: if the optional API is offline, Arc-RAR is missing, or a provider returns invalid state, it shows an offline/error payload rather than inventing backend truth.


## Companion hardware endpoint

For ESP32 and Arduino-class display nodes, use the compact companion payload instead of the full dashboard payload:

```bash
ai-meter companion-status --provider mock
```

Or from the local API:

```text
GET /companion/status?provider=mock
GET /companion/status?provider=arcrar-cli
```

Example compact payload:

```json
{
  "schema": "ai_desk_meter_companion_v1",
  "status": "linked",
  "current_pct": 50,
  "weekly_pct": 11,
  "current_reset": "1h 22m",
  "weekly_reset": "6d 8h",
  "activity": "musing",
  "message": "✶ Musing...",
  "backend": "mock",
  "warnings": 0,
  "errors": 0
}
```

The companion endpoint is display-safe and intentionally small. Backend authority remains on desktop, Raspberry Pi/Linux SBC, Arc-RAR, or future ARC/Omnibinary provider layers.

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

The firmware scaffold is intentionally board-adaptation friendly. Start from your board vendor's display example, then wire the JSON parser and renderer into the provided module layout. v0.6 also includes standalone example sketches under `firmware/esp32_companion_display/` and `firmware/arduino_serial_companion/`.

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
│  ├─ arcrar-cli-contract.md
│  ├─ arcrar-fixtures.md
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
- **v0.6** ESP32 / Arduino companion bridge ✅
- **v0.7** Arc-RAR CLI command compatibility pass ✅
- **v0.8** Native dashboard shell prototype
- **v1.0** Stable Arc-RAR-backed AI Desk Meter
- **v1.1+** Omnibinary adapter, ARC-Core hardwire integration, archive timeline view, Neural Synth toggle page
- **v3.0** MuseMeter commercial full package: second-brain / Neural Synth / AI buddy product
- **Future provider targets** Multi-AI desk meter support where official/local signals exist: Claude Code/manual logs, Codex-style CLI workflows, Gemini CLI-style workflows, Ollama/local LLMs, and other local-first provider adapters

## Validation

Current package validation:

```text
pytest passes locally for the included protocol, provider, API, diagnostics, deployment, companion, and Arc-RAR CLI contract tests
mock provider works
state-file Arc-RAR provider works
Arc-RAR CLI provider fails closed for missing executable, invalid JSON, non-zero exit, and timeout
Arc-RAR CLI provider now merges status, latest receipt, archive verify, and session inspect fixture outputs
file/stdout payload commands work without a local server
optional local API bridge works for `/health`, `/providers`, `/status`, `/companion/status`, and `/diagnostics`
diagnostics ZIP export works without including secrets or private prompt/session content
Linux/SBC install script, smoke-test script, systemd unit, kiosk docs, and network-safety docs are included
```

## License

MIT for the current open-source corridor. See `LICENSE` and `docs/licensing-roadmap.md`. The planned MuseMeter 3.0 package is intended to move to a commercial license after the open foundation is stable.


## v0.9 Omnibinary adapter boundary

The repo now includes a planned, fails-closed `omnibinary` provider and adapter documentation. This does not claim Omnibinary is fully wired yet. It locks the safe connection boundary for future binary event-spine, replay ledger, and second-brain substrate work.

```bash
ai-meter status --provider omnibinary
AI_METER_OMNIBINARY_STATE=examples/omnibinary_event_state.example.json ai-meter status --provider omnibinary
```

Current authority order remains:

```text
ARC-Core = canonical authority
Arc-RAR = portable archive / receipt bundle backend
Omnibinary = future binary event spine / replay mirror
AI Desk Meter = dashboard, companion payloads, diagnostics
Neural Synth = later visualization toggle driven by real provider state
MuseMeter 3.0 = later commercial second-brain / Neural Synth / AI buddy package
```


## v1.1.6 — Runtime Dashboard Button

- Adds a Dashboard button for the live runtime dashboard IP page.
- Docs opens the docs page/site.
- The runtime page continues to auto-refresh from `runtime/status.json` and mirror source-of-truth state.

## v1.1.4 — Connection Dot + Unified Runtime Docs Panel

- Added red/green connection indicator to the runtime page.
- Integrated docs/runtime/connection info into the same page with a Back to Muse button.
- Browser/Vite preview and the app holster now use the same runtime page UX.
- Runtime page auto-refreshes from `runtime/status.json` as the source of truth.


### v1.1.6 Runtime/Muse state model

The top-right connection dot indicates the CLI/runtime writer and runtime dashboard IP page are reachable. It does not mean a Muse/model/agent is active. `No active Muse` remains until a payload reports `muse_connected: true`, `agent_connected: true`, `active_muse: true`, or an active `muse_state`.


## v1.1.7 runtime dashboard clarification

The runtime connection dot means the CLI/runtime writer and runtime dashboard path are reachable. It does not mean a Muse/model/agent is active. Mock/runtime-only payloads keep the UI on **No active Muse** while still showing a green runtime connection. DIY hardware specs and cost/BOM details are now visible directly from the runtime dashboard and docs page.


## v1.1.8 parts and sourcing completion

The DIY hardware path now includes a build-ready sourcing page at `docs/parts-and-sourcing.md`. It documents the recommended Waveshare ESP32-S3-Touch-AMOLED-2.16 board, required USB-C/runtime-host parts, optional enclosure/battery/fastener parts, cost tiers, search terms, and source categories. The runtime dashboard DIY / Cost Specs panel exposes the same buying guidance so users do not have to guess what to purchase.


## v1.1.9

Smooth runtime stream patch: no flicker between disconnected/connected during transient reads; blink timers survive dashboard refreshes.


## v1.2.1 — Stable Runtime App Shell

The runtime dashboard now separates static controls from live payload streaming. Buttons, tabs, docs/specs navigation, and layout containers render once; the 0.5s refresh loop updates only values, logs, JSON, and status text. This prevents the two-truth flicker and button reflow seen in the v1.1 line.
