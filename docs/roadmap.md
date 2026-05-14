# Roadmap

## v0.1 — Clean dashboard and mock/manual providers ✅

- Stable payload schema
- Mock provider
- Manual provider
- Stdout and Wi-Fi transports
- Public documentation cleanup

## v0.2 — Arc-RAR state-file provider ✅

- Read local Arc-RAR state JSON
- Fail closed on missing/corrupt state
- Surface backend receipt/archive/hardwire status
- Add examples and tests

## v0.3 — Arc-RAR CLI/API provider ✅

- Consume `arc-rar status --json` through `arcrar-cli`
- Add timeout/error handling
- Add missing-executable handling
- Add invalid JSON/non-zero exit tests
- Keep state-file provider as the development bridge

## v0.4 — Live dashboard refresh and diagnostics export ✅

- Local HTTP API
- Live dashboard provider polling
- Diagnostics ZIP export
- Offline/error-safe dashboard behavior

## v0.5 — Raspberry Pi / Linux SBC validation ✅

- Install and smoke-test scripts
- systemd service template
- kiosk/local-dashboard docs
- network safety guidance

## v0.6 — ESP32 / Arduino companion bridge ✅

- Compact companion endpoint: `/companion/status`
- `ai-meter companion-status` command
- ESP32 companion display example firmware
- Arduino-class serial companion example firmware
- Companion protocol docs and payload examples
- Tests for compact payload conversion and endpoint behavior

## v0.7 — Arc-RAR command compatibility pass ✅

- Document required `arc-rar status --json` output contract
- Document optional enrichment commands: `receipts latest`, `archive verify`, and `session inspect`
- Add fixture examples for valid, warning, error, receipt, archive, and session output
- Merge status, receipt, archive, and session outputs into one dashboard-safe payload
- Treat required status failures as offline/error states
- Treat optional enrichment failures as warnings

## v0.8 — Native dashboard shell prototype ✅

- Tauri shell plan and config example
- Desktop security notes
- Frontend bridge contract for the local API
- macOS/Linux and Windows dashboard launch scripts
- Artifact tests to preserve the native shell path

## v0.9 — Omnibinary adapter spec

- Define Omnibinary as an optional event-spine adapter
- Keep Arc-RAR as archive/receipt packaging authority
- Document adapter payload contract before implementation
- Do not add Neural Synth visualization until real state exists

## v1.0 — Stable open-source AI Desk Meter

- Cross-platform local host path
- Raspberry Pi/SBC deployment path
- ESP32/Arduino companion examples
- Arc-RAR provider boundary
- Live dashboard refresh
- Diagnostics export
- Honest offline/error states

## v1.1+ — Omnibinary and ARC-Core expansion

- Omnibinary event-spine adapter
- ARC-Core canonical hardwire integration
- Archive/replay timeline view
- Neural Synth toggle page driven by real state

## v3.0 — MuseMeter commercial package

MuseMeter 3.0 is the planned commercial-licensed full package after the open-source foundation is stable. Direction: second-brain / Neural Synth / AI buddy package using the open dashboard, provider, hardware, and backend lessons from v0.x-v2.x.

The baseline pixel buddy and `✶ Musing...` state remain intentional. For now, Musing means prompt response or action-loading. Later versions can differentiate states such as verifying, archiving, warning, responding, and idle.


## v0.9 — Omnibinary adapter boundary

Status: complete for the open-source foundation.

- Added a fails-closed `omnibinary` provider.
- Added Omnibinary fixture examples.
- Added the ARC-Core hardwire map.
- Added adapter boundary documentation.
- Kept Neural Synth as a later visualization layer driven by real provider state.

## v1.0 — Stable open-source functional release

Next release target. Focus on final public polish, install validation, release notes, and packaging hygiene.
