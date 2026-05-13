# Host App Guide

The host app runs on the user's computer. It reads usage signals, normalizes them, and sends one payload to the device.

## Providers

- `mock`: moving fake values for testing
- `manual`: fixed/manual config values
- future `local_logs`: local user-owned logs where available
- future `official_api`: official API usage endpoints where available

## Transports

- `stdout`: prints payloads for debugging
- `wifi`: HTTP POST to the ESP32
- future `ble`: BLE characteristic write

## Examples

```bash
ai-meter test-payload
ai-meter start --provider mock --transport stdout
ai-meter start --provider mock --transport wifi --url http://192.168.1.44/api/state
```
