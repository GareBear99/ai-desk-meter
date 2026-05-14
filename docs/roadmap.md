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

## v0.7 — Arc-RAR command compatibility pass

- Validate against the real Arc-RAR CLI package
- Confirm `arc-rar status --json` output contract
- Add fixture tests from real backend output
- Document supported Arc-RAR command versions

## v0.8 — Native dashboard shell prototype

- Package local dashboard as desktop shell
- Add provider health view
- Add archive/receipt view
- Add diagnostics export button

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
