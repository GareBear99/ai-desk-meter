# AI Desk Meter v1.0.1 — Offline-First Runtime Correction

v1.0.1 keeps the stable v1.0 open-source foundation and corrects the default runtime model: AI Desk Meter does not require a local server.

## Added

- `ai-meter write-status --provider mock --out runtime/status.json`
- `ai-meter write-companion --provider mock --out runtime/companion.json`
- `ai-meter watch --provider mock --out runtime/status.json --interval 2`
- `ai-meter watch-companion --provider mock --out runtime/companion.json --interval 2`
- Atomic JSON file writes for dashboard and companion payloads.
- Offline-first documentation in `docs/no-local-server-default.md`.
- Dashboard file-import workflow so `docs/index.html` can be used without a running API server.

## Preserved

- Optional local API for development/debug preview.
- Arc-RAR state-file provider.
- Arc-RAR CLI provider contract.
- Omnibinary fails-closed adapter boundary.
- Raspberry Pi / Linux SBC deployment path.
- ESP32/Arduino companion bridge.
- Pixel buddy and `✶ Musing...` baseline state.

## Rule

Default mode is file/stdout/serial-friendly. The local server is optional.
