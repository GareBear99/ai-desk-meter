# Firmware Guide

## Target

Primary endpoint target: ESP32-S3 with a 480×480 AMOLED display.

Secondary endpoint target: Arduino-class boards with simplified serial/display payloads.

## Stack

- PlatformIO
- Arduino ESP32 core
- ArduinoJson
- Vendor display example first
- Optional LVGL/LovyanGFX once display is stable

## Firmware states

- `BOOT`: startup and self-test
- `PAIRING`: no configured host
- `ONLINE`: valid payload received
- `STALE`: no recent payload
- `OFFLINE`: host missing for several minutes
- `ERROR`: bad payload or runtime problem

## Integration note

Display drivers are board-specific. This repo includes placeholders and a console-safe scaffold. Use your board's vendor display example as the base, then connect `UsageState` and `UiRenderer`.

For Arduino-class companion devices, keep the payload smaller and treat the board as a display/telemetry endpoint only.
