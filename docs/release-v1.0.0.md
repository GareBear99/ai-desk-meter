# AI Desk Meter v1.0.0 Release Notes

AI Desk Meter v1.0.0 is the first stable open-source functional release. It provides a local host, validated payload protocol, local API, browser dashboard refresh path, Arc-RAR bridge providers, diagnostics export, Raspberry Pi/SBC deployment notes, compact ESP32/Arduino companion payloads, and a native shell prototype boundary.

## Included

- Mock/manual providers for safe local demos.
- Arc-RAR state-file provider for fixture-based integration testing.
- Arc-RAR CLI provider with required `status --json` command and optional receipt/archive/session enrichment commands.
- Omnibinary provider boundary that fails closed unless fixture state is supplied.
- Local API: `/health`, `/providers`, `/status`, `/companion/status`, `/diagnostics`.
- CLI: `status`, `start`, `serve`, `companion-status`, `diagnostics`, `doctor`, `providers`, `version`.
- Diagnostics ZIP export designed to exclude secrets, tokens, prompts, and private session content.
- Raspberry Pi/Linux SBC install and smoke-test path.
- ESP32/Arduino companion-display examples.
- Tauri-oriented native dashboard shell plan/prototype docs.

## Not included

- No usage-limit bypassing.
- No account rotation.
- No private dashboard scraping.
- No fake exact Claude/API usage numbers.
- No fully wired Omnibinary backend yet.
- No Neural Synth state visualization yet.
- No MuseMeter 3.0 commercial feature set yet.

## Product path

The v0.x-v2.x corridor remains the open-source foundation. The planned MuseMeter 3.0 package is the later commercial second-brain / Neural Synth / AI buddy product built on the stable open foundation.
