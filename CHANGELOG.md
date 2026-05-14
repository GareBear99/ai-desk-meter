# Changelog

## 0.6.0 - Companion hardware bridge

- Added compact companion payload conversion and `/companion/status` endpoint.
- Added `ai-meter companion-status --provider ...` command.
- Added ESP32 companion display example sketch.
- Added Arduino-class serial companion example sketch.
- Added companion payload examples and hardware companion protocol docs.
- Added tests for compact payload conversion, companion endpoint, and firmware artifacts.

## 0.5.0 - Raspberry Pi/SBC deployment and MuseMeter path

- Added Linux/SBC install and smoke-test scripts.
- Added systemd service template and example environment file.
- Added Raspberry Pi setup, Linux SBC validation, network security, kiosk, and companion bridge docs.
- Restored and preserved the pixel buddy / `✶ Musing...` loading/responding state as intentional product identity.
- Added licensing roadmap: v0.x-v2.x open-source corridor, planned MuseMeter 3.0 commercial full package.
- Updated public dashboard copy for the MuseMeter 3.0 second-brain / Neural Synth / AI buddy direction without moving those features into the current backend milestone.

## 0.4.0 - Local API and diagnostics

- Added local HTTP API bridge: `/health`, `/providers`, `/status`, and `/diagnostics`.
- Added dashboard live-refresh panel for local provider polling.
- Added safe diagnostics ZIP export command.
- Added local API and dashboard refresh documentation.
- Added tests for server endpoints and diagnostics export.

## 0.3.0 - Arc-RAR CLI provider milestone

- Added `arcrar-cli` provider for timeout-safe `arc-rar status --json` integration.
- Added fail-closed handling for missing executable, timeout, non-zero exit, invalid JSON, and validation errors.
- Added `ai-meter status --provider ...` command for formatted one-shot provider inspection.
- Added CLI provider tests and example Arc-RAR CLI status payload.
- Updated provider contract, Arc-RAR integration spec, roadmap, test matrix, and release checklist.

## 0.1.0 - Initial DIY repo scaffold

- Added full HTML spec guide.
- Added host daemon scaffold with mock/manual providers.
- Added Wi-Fi/stdout transports.
- Added ESP32-S3 firmware scaffold.
- Added JSON protocol examples and docs.
- Added enclosure and testing documentation.
