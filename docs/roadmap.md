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

- Consume stable Arc-RAR JSON commands
- Add timeout/error handling
- Add diagnostics export
- Add backend health panel

## v0.4 — Provider contract testing

- Mock/manual/arcrar provider tests
- Protocol validation tests
- Offline/error-state tests
- Dashboard stale-state tests

## v0.5 — Raspberry Pi / Linux SBC validation

- Document Raspberry Pi install path
- Validate kiosk/local-dashboard mode
- Add lightweight service template
- Test low-resource operation

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
