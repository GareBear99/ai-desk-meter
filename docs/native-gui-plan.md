# Native GUI Plan

AI Desk Meter v0.8 adds a desktop-shell path without moving authority into the interface. The native shell is a wrapper around the already-tested local host service and dashboard assets.

## Core rule

The GUI is a viewer and control surface. Provider truth remains in the host process and backend integrations such as Arc-RAR.

```text
Arc-RAR / mock / manual provider
        ↓
ai-meter local API
        ↓
HTML dashboard / Tauri shell / kiosk view
```

## Open-source track

The v0.x-v2.x track stays open-source and focuses on local API stability, provider contract stability, Raspberry Pi / Linux SBC operation, ESP32/Arduino-class companion displays, dashboard shelling, and diagnostics.

## MuseMeter 3.0 track

MuseMeter 3.0 is the planned commercial-licensed full package after the open foundation is stable. Its direction is a second-brain / Neural Synth / AI buddy product. The current pixel buddy and `✶ Musing...` state remain intentional; for now, Musing means prompt response or action loading.

## v0.8 desktop shell scope

Included in this repo stage:

- Tauri shell plan and config example
- launch scripts for macOS/Linux and Windows
- desktop security notes
- frontend bridge notes for polling the local API
- artifact tests to prevent losing the native shell path

Not included yet: compiled desktop binaries, signed installers, Omnibinary adapter, Neural Synth toggle implementation, or commercial MuseMeter-only features.
