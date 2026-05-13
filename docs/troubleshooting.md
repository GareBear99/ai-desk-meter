# Troubleshooting

## Device does not update

- Confirm the ESP32 and computer are on the same LAN.
- Confirm the device URL/IP.
- Run `ai-meter start --transport stdout` first.
- Try posting `examples/sample_payload.json` manually.

## Bad JSON shown on device

- Validate against `docs/protocol.md`.
- Confirm percentages are numbers, not strings.
- Confirm `schema` is present.

## Usage looks wrong

- Check the confidence field.
- Use manual/mock provider to isolate device issues.
- Do not treat estimated provider output as exact.
