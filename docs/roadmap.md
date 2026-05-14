# Roadmap

## v0.1 — Clean dashboard and mock/manual providers

- Stable payload schema
- Mock provider
- Manual provider
- Stdout and Wi-Fi transports
- Public documentation cleanup

## v0.2 — Arc-RAR state-file provider

- Read local Arc-RAR state JSON
- Fail closed on missing/corrupt state
- Surface backend receipt/archive/hardwire status
- Add examples and tests

## v0.3 — Arc-RAR CLI/API provider

- Consume `arc-rar status --json` through `arcrar-cli`
- Add timeout/error handling
- Add missing-executable handling
- Add invalid JSON/non-zero exit tests
- Keep state-file provider as the development bridge

Status: implemented in host provider layer.

## v0.4 — Live dashboard refresh and diagnostics export ✅

- Add a small local endpoint or generated payload file for the dashboard
- Refresh provider output without reloading the page
- Show stale/offline/error states visibly
- Add a diagnostic bundle export command
- Add backend health panel

## v0.4b — Provider contract testing

- Mock/manual/arcrar provider tests
- Protocol validation tests
- Offline/error-state tests
- Dashboard stale-state tests

## v0.5 — Raspberry Pi / Linux SBC validation ✅

- Document Raspberry Pi install path ✅
- Add install and smoke-test scripts ✅
- Validate kiosk/local-dashboard mode path ✅
- Add lightweight systemd service template ✅
- Add loopback-first network security guidance ✅
- Test low-resource operation on physical target hardware next

## v0.6 — ESP32-S3 display endpoint hardening

- Confirm board-specific display driver path
- Improve Wi-Fi endpoint behavior
- Add stale/offline rendering
- Add self-test screen

## v0.7 — Arduino-class companion bridge

- Define simplified serial payload
- Add compact telemetry/display example
- Document Arduino-class limits honestly
- Keep backend authority on desktop/SBC/Arc-RAR

## v0.8 — Native dashboard shell prototype

- Package local dashboard as desktop shell
- Add provider health view
- Add archive/receipt view
- Add diagnostics export button

## v1.0 — Stable Arc-RAR-backed AI Desk Meter

- Backend state is verifiable
- Dashboard state is validated
- Cross-platform path is documented
- Device endpoint path is documented
- Tests cover normal/offline/error cases

## v1.1+ — Omnibinary and ARC-Core expansion

- Omnibinary event-spine adapter
- ARC-Core canonical hardwire integration
- Archive/replay timeline view
- Neural Synth toggle page driven by real state


## v3.0 — MuseMeter commercial package

MuseMeter 3.0 is the planned commercial-licensed full package after the open-source foundation is stable. Direction: second-brain / Neural Synth / AI buddy package using the open dashboard, provider, hardware, and backend lessons from v0.x-v2.x.

The baseline pixel buddy and `✶ Musing...` state remain intentional. For now, Musing means prompt response or action-loading. Later versions can differentiate states such as verifying, archiving, warning, responding, and idle.
