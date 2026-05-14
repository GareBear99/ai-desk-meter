# AI Desk Meter Documentation

This folder powers the public GitHub Pages landing page and project documentation.

Public page target:

https://garebear99.github.io/ai-desk-meter/

Recommended reading order:

1. `architecture.md`
2. `provider-contract.md`
3. `arcrar-integration-spec.md`
4. `hardware.md`
5. `firmware.md`
6. `host-app.md`
7. `test-matrix.md`
8. `roadmap.md`
9. `neural-synth-roadmap.md`


## Current implementation note

The host package now includes both `arcrar` for state-file bridge testing and `arcrar-cli` for timeout-safe `arc-rar status --json` integration. Use `ai-meter status --provider arcrar-cli` to inspect the live CLI provider boundary.


## Functional local bridge

- [Local API](local-api.md)
- [Dashboard refresh](dashboard-refresh.md)


## Added deployment and product-direction docs

- `raspberry-pi-setup.md` — Raspberry Pi / Linux SBC install and service path
- `linux-sbc-validation.md` — hardware validation checklist
- `network-security.md` — loopback-first and LAN binding guidance
- `companion-bridge.md` — ESP32 / Arduino companion display bridge direction
- `licensing-roadmap.md` — open-source corridor and MuseMeter 3.0 commercial package direction
- `character-spec.md` — pixel buddy and `✶ Musing...` state preservation
