# Changelog

## 0.1.0 - Initial DIY repo scaffold

- Added full HTML spec guide.
- Added host daemon scaffold with mock/manual providers.
- Added Wi-Fi/stdout transports.
- Added ESP32-S3 firmware scaffold.
- Added JSON protocol examples and docs.
- Added enclosure and testing documentation.

## 0.3.0 - Arc-RAR CLI provider milestone

- Added `arcrar-cli` provider for timeout-safe `arc-rar status --json` integration.
- Added fail-closed handling for missing executable, timeout, non-zero exit, invalid JSON, and validation errors.
- Added `ai-meter status --provider ...` command for formatted one-shot provider inspection.
- Added CLI provider tests and example Arc-RAR CLI status payload.
- Updated provider contract, Arc-RAR integration spec, roadmap, test matrix, and release checklist.
