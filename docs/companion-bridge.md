# ESP32 / Arduino Companion Bridge

AI Desk Meter supports small hardware endpoints as companion displays. The full backend authority remains on the desktop, Raspberry Pi, Linux SBC, or Arc-RAR-backed host.

## Intended companion roles

- small OLED/AMOLED usage display
- “Musing...” status indicator
- warning/error indicator
- receipt/archive health light
- serial or Wi-Fi payload display

## Not intended roles

Arduino-class microcontrollers should not be treated as:

- the source of backend truth
- the receipt archive authority
- the full dashboard server
- the Arc-RAR host process

## Bridge payload

The full API payload can be compacted for microcontrollers:

```json
{
  "schema": "ai-desk-meter.compact.v1",
  "current": 50,
  "weekly": 11,
  "mode": "musing",
  "status": "Musing...",
  "warn": false,
  "error": false
}
```

The compact bridge should be derived from the validated host payload, not independently guessed by firmware.
