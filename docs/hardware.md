# Hardware Guide

AI Desk Meter supports multiple hardware roles. The full backend should run on a desktop/laptop or Raspberry Pi-class Linux system. Small microcontrollers should be used as displays or companion telemetry endpoints.

## Recommended first physical display

The closest first target is a Waveshare ESP32-S3 AMOLED board, especially the 2.16-inch 480×480 model.

Expected useful features:

- ESP32-S3 microcontroller
- 480×480 AMOLED display
- Wi-Fi
- Bluetooth LE
- USB-C programming/power
- 16 MB flash and PSRAM on many variants
- Touch support on supported models

## Raspberry Pi / SBC target

A Raspberry Pi or similar Linux SBC can run the host daemon directly and act as an always-on local dashboard/kiosk.

Recommended uses:

- Desk dashboard appliance
- Local bridge between Arc-RAR and display nodes
- Wi-Fi/serial/BLE payload broadcaster
- Small touchscreen dashboard

## Arduino-class target

Arduino-class microcontrollers should be treated as simplified endpoints.

Good roles:

- Serial display node
- LED/buzzer warning indicator
- Tiny OLED/LCD state display
- Local button/input companion

Not recommended:

- Running the full Python host daemon
- Acting as the authoritative backend
- Parsing large diagnostic bundles

## First-build rule

Buy the integrated ESP32-S3 display board first. Do not start by wiring a separate ESP32 and display unless you specifically want an electronics project.

## Power

Use USB-C desk power for v0.1. Battery support adds charging, enclosure, heat, and safety complexity.

## Enclosure

Start with a wedge stand or simple 3D printed frame. Measure the exact board before printing.
