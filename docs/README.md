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

- [Optional local API](local-api.md)
- [Dashboard refresh](dashboard-refresh.md)


## Added deployment and product-direction docs

- `raspberry-pi-setup.md` — Raspberry Pi / Linux SBC install and service path
- `linux-sbc-validation.md` — hardware validation checklist
- `network-security.md` — loopback-first and LAN binding guidance
- `companion-bridge.md` — ESP32 / Arduino companion display bridge direction
- `licensing-roadmap.md` — open-source corridor and MuseMeter 3.0 commercial package direction
- `character-spec.md` — pixel buddy and `✶ Musing...` state preservation

## Native shell

- [Native GUI plan](native-gui-plan.md)
- [Tauri shell plan](tauri-shell-plan.md)
- [Desktop security notes](desktop-security.md)


- [Omnibinary Adapter Spec](omnibinary-adapter-spec.md)
- [ARC-Core Hardwire Map](arc-core-hardwire-map.md)
- [Adapter Boundaries](adapter-boundaries.md)

## v1.0 release docs

- [Install and run](install.md)
- [Release notes v1.0.0](release-v1.0.0.md)
- [Functional release definition](functional-release.md)
- [Open-source boundary](open-source-boundary.md)
- [Version and license matrix](version-license-matrix.md)


## v1.0.1 No-server default

AI Desk Meter does not require a local server for normal use. Prefer `write-status`, `write-companion`, `watch`, and `watch-companion` for desktop, Raspberry Pi, native/Tauri, and companion-device flows. The HTTP API remains optional development/debug preview tooling.

- [v1.0.2 release notes](release-v1.0.2.md) — native Tauri/Rust desktop app release notes.
- [v1.0.3 release notes](release-v1.0.3.md) — animated Musing state and runtime action layer.
- [v1.0.6 release notes](release-v1.0.6.md) — corrected No active Muse preview behavior and eye-only blinking.
- [v1.0.4 release notes](release-v1.0.4.md) — explicit No active Muse disconnected-state behavior.

- [v1.0.7 release notes](release-v1.0.7.md) — exact `No Muse.` label inside the actual SVG disconnected state.
- [v1.0.6 release notes](release-v1.0.6.md) — native SVG eye blink fix and faster no-server runtime refresh.

- [v1.1.2 native holster dev browser view](release-v1.1.2.md)

- [v1.1.2 unified runtime/dev page](release-v1.1.2.md)


## v1.1.6

- [v1.1.6 runtime dashboard button](release-v1.1.6.md)

## v1.1.4 — Runtime Docs Button Fix

- [v1.1.4 runtime docs button fix](release-v1.1.4.md)

## v1.1.3 — Connection Dot + Unified Runtime Docs Panel

- Added red/green connection indicator to the runtime page.
- Integrated docs/runtime/connection info into the same page with a Back to Muse button.
- Browser/Vite preview and the app holster now use the same runtime page UX.
- Runtime page auto-refreshes from `runtime/status.json` as the source of truth.


### v1.1.6 Runtime/Muse state model

The top-right connection dot indicates the CLI/runtime writer and runtime dashboard IP page are reachable. It does not mean a Muse/model/agent is active. `No active Muse` remains until a payload reports `muse_connected: true`, `agent_connected: true`, `active_muse: true`, or an active `muse_state`.

- [Parts & Sourcing](parts-and-sourcing.md) — build-ready buying guide, costs, search terms, and source categories.

## v1.1.8

- [v1.1.8 parts and sourcing completion](release-v1.1.8.md)
- [Parts & Sourcing](parts-and-sourcing.md)


## v1.1.9

Smooth runtime stream patch: no flicker between disconnected/connected during transient reads; blink timers survive dashboard refreshes.


## v1.2.1 — Stable Runtime App Shell

The runtime dashboard now separates static controls from live payload streaming. Buttons, tabs, docs/specs navigation, and layout containers render once; the 0.5s refresh loop updates only values, logs, JSON, and status text. This prevents the two-truth flicker and button reflow seen in the v1.1 line.
