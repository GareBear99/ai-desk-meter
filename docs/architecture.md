# Architecture

AI Desk Meter is a local-first dashboard and device bridge for AI workflow visibility. Its architecture is intentionally separated into provider, protocol, transport, and display layers.

## Design principles

1. **Backend truth first** — providers report state; dashboards do not invent it.
2. **Local-first operation** — the default path should work without a hosted service.
3. **Portable endpoints** — desktop, Raspberry Pi, ESP32, and Arduino-class nodes should all have appropriate roles.
4. **Honest confidence levels** — exact, estimated, mock, and unknown states must be visible.
5. **Fail closed** — missing or corrupt backend state becomes an error/offline payload, not a guessed success state.

## Layer model

```text
Provider source
  ├─ mock/manual
  ├─ Arc-RAR state file
  ├─ future Arc-RAR CLI/API
  ├─ future local logs
  └─ future Omnibinary event spine
        ↓
Provider contract
        ↓
UsagePayload validation
        ↓
Transport
  ├─ stdout
  ├─ Wi-Fi POST
  ├─ future BLE
  └─ future serial/MQTT bridge
        ↓
Display/control surfaces
  ├─ HTML dashboard
  ├─ Raspberry Pi kiosk
  ├─ ESP32-S3 meter
  ├─ Arduino-class companion display
  └─ future native GUI
```

## Device class responsibilities

### Desktop/laptop

Runs the full host daemon, provider adapters, validation, diagnostics, and future native GUI.

### Raspberry Pi / Linux SBC

Runs the full Python host daemon and can act as a kiosk, bridge, or always-on local control node. This is the preferred low-cost deployment target for a standalone desk appliance.

### ESP32-S3

Receives compact JSON payloads and renders local display state. It should not be treated as the backend authority.

### Arduino-class microcontrollers

Arduino-class devices can be used as small display/telemetry companions over serial, I2C, BLE, LoRa, or compact JSON/CBOR-style payloads. They should not run the full Python backend.

## Arc-RAR role

Arc-RAR is the portable archive/receipt backend target. AI Desk Meter should surface Arc-RAR state such as receipt availability, archive verification, hardwire portability, latest checkpoint, and validation errors.

## Omnibinary role

Omnibinary is a future event-spine and replay adapter. It should be added after Arc-RAR provider contracts and tests are stable.

## Neural Synth role

Neural Synth is a future visualization toggle page. It should visualize real provider/session/archive state, not decorative fake data.
