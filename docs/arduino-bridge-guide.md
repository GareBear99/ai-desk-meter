# Arduino-Class Companion Guide

Arduino-class boards are supported as simplified companion nodes. They are not expected to run the full Python host, Arc-RAR provider, dashboard, or diagnostics stack.

Supported roles:

- serial display node
- simplified OLED/LCD meter
- LED/buzzer status indicator
- telemetry relay from Raspberry Pi or desktop host

Recommended flow:

```text
AI Desk Meter host → companion payload → serial line / Wi-Fi bridge → Arduino display
```

For small boards, prefer the compact payload from `/companion/status` or the minified example in `examples/companion_payload.min.json`.
