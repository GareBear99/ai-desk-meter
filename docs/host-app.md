# Host App Guide

The host app runs on a desktop, laptop, or Raspberry Pi-class Linux system. It reads local signals, normalizes them, and sends one payload to a dashboard or device.

## Providers

- `mock`: moving demo values for testing
- `manual`: fixed/manual config values
- `arcrar`: local Arc-RAR state-file bridge
- future `arcrar-cli`: stable Arc-RAR CLI/API adapter
- future `local_logs`: local user-owned logs where available
- future `omnibinary`: event-spine adapter after Arc-RAR is stable

## Transports

- `stdout`: prints payloads for debugging
- `wifi`: HTTP POST to the ESP32 or local dashboard endpoint
- future `ble`: BLE characteristic write
- future `serial`: Arduino-class companion bridge

## Examples

```bash
ai-meter test-payload
ai-meter providers
ai-meter start --provider mock --transport stdout --once
ai-meter start --provider mock --transport wifi --url http://192.168.1.44/api/state
```

Arc-RAR bridge:

```bash
AI_METER_ARCRAR_STATE=../examples/arcrar_meter_state.example.json   ai-meter start --provider arcrar --transport stdout --once
```
