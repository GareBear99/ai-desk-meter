# Changelog

## v1.0.0 — Stable open-source functional release

- Promoted the package version to 1.0.0.
- Added `ai-meter version` and `ai-meter doctor --provider ...` commands.
- Added v1.0 release notes, install guide, open-source boundary, functional release definition, and version/license matrix.
- Added release smoke-test script and GitHub Actions CI workflow.
- Kept MuseMeter 3.0 documented as the future commercial second-brain / Neural Synth / AI buddy package while preserving the current open-source foundation.
- Preserved the intentional pixel buddy and `✶ Musing...` state.

## v0.9.0 — Omnibinary adapter boundary

- Added planned/fails-closed Omnibinary provider.
- Added Omnibinary adapter spec and fixtures.
- Added ARC-Core hardwire map.
- Added adapter boundary rules.
- Registered `omnibinary` provider without claiming full backend integration.


## 0.8.0 - Native dashboard shell prototype

- Added Tauri-oriented native shell plan and configuration example.
- Added desktop security notes and frontend bridge docs for the local API.
- Added macOS/Linux and Windows launch scripts for the local dashboard service.
- Added native artifact tests so the desktop path is preserved.
- Kept GUI authority separate from provider/backend truth and preserved the open-source path toward MuseMeter 3.0.

## 0.7.0 - Arc-RAR CLI command compatibility pass

- Expanded the Arc-RAR CLI provider from a single status command to a contract bundle.
- Required command: `arc-rar status --json`.
- Optional enrichment commands: `arc-rar receipts latest --json`, `arc-rar archive verify --json`, and `arc-rar session inspect --json`.
- Added command contract docs and Arc-RAR fixture docs.
- Added valid/warning/error status fixtures plus receipt, archive verify, and session inspect fixtures.
- Added contract tests for merged backend state, optional command warnings, required command invalid JSON, and failed archive verification.

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
