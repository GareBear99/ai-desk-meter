## v1.2.1 - Runtime dashboard IP server fix

- Fixed Dashboard button opening a refused `127.0.0.1:1420` page when Vite was not running.
- Added built-in Electron holster HTTP server for the runtime dashboard IP site.
- Added `/runtime/status.json` and `/health` routes served directly from the source-of-truth runtime payload.
- Kept Electron app window and external browser dashboard in sync from the same payload.

## v1.2.0 — Stable Runtime App Shell

- Fixed runtime dashboard button/tab flicker by isolating static controls from payload refresh.
- Runtime polling now updates text/value nodes only instead of repainting navigation controls.
- Replaced status-title rebuilds with stable spans for star/status/dots.
- Added fixed control-bar layout so Dashboard / Docs / DIY buttons do not jump during streaming.
- Preserved runtime-vs-Muse truth model and smooth runtime/status.json source-of-truth flow.

## v1.1.9 — Smooth Runtime Stream

- Fixed flashing/two-truth behavior by holding the last good runtime payload across transient file-read misses.
- Prevented overlapping dashboard refresh calls.
- Stopped SVG blink timers from resetting every refresh.
- Smoothed bar/card visual updates for the runtime dashboard.
- Preserved runtime-connected vs Muse-connected separation.

## v1.1.6 — Runtime Connection vs Muse State

## 1.1.8 — Parts & Sourcing Completion

- Added `docs/parts-and-sourcing.md` with required/optional parts, cost tiers, source categories, and search terms.
- Expanded runtime dashboard DIY / Cost Specs panel with buying guidance and sourcing table.
- Added Parts & Sourcing links to docs and app/runtime panels.
- Clarified that ESP32/Arduino-class boards are companion endpoints while the host/Pi remains the runtime source of truth.


- Split runtime connectivity from Muse/model connectivity.
- Top-right dot now means CLI/runtime + runtime dashboard IP page are reachable.
- No active Muse only changes when a real Muse/model/agent payload is connected.
- Updated SVG-eye blink rules: 3–11s idle blink, usage-aware active Muse blink.

## v1.1.5 — Runtime Dashboard Button

- Added Dashboard button that opens the live runtime dashboard IP page (`http://127.0.0.1:1420/#muse`).
- Electron holster now starts/opens the browser runtime dashboard from the Dashboard button.
- Docs button now opens the docs page/site instead of reusing the same runtime panel.
- Runtime dashboard keeps polling `runtime/status.json` and mirrors the source-of-truth payload with the red/green connection dot.

## v1.1.4 — Runtime Docs Button Fix

- Fixed `Docs / Runtime Info` so it opens the integrated docs/runtime panel from both the Electron holster and external browser/Vite page.
- Fixed the removed `devBrowserButton` reference that could stop runtime page controls from binding.
- Added `Back to Muse` behavior that reliably returns to the Muse dashboard panel.
- Added optional full-docs opener wiring for shells that support it.


## v1.1.3 — Connection Dot + Unified Runtime Docs Panel

- Added red/green connection indicator to the runtime page.
- Integrated docs/runtime/connection info into the same page with a Back to Muse button.
- Browser/Vite preview and the app holster now use the same runtime page UX.
- Runtime page auto-refreshes from `runtime/status.json` as the source of truth.

## v1.1.2 — Unified runtime/dev page

- Merged runtime connection, Dev JSON, internal commands, provider/Omnibinary boundary, and logs into the same runtime page.
- The Electron native holster and the external browser/Vite preview now use the same page and same panels.
- The former separate `runtime/dev-connection.html` report is no longer the main UX path.
- The Electron button now opens the same runtime page externally with `#dev` instead of generating a separate dev page.
- Keeps no-server runtime JSON as the default and the local API as optional dev/debug tooling only.

# Changelog

## v1.1.1 — Native holster dev browser view

- Added Electron holster button to open a browser dev view.
- Generated `runtime/dev-connection.html` with connection state, current payload JSON, app info, internal commands, optional local API routes, and provider boundary details.
- Added resilient launcher fallback: `ai-meter app` opens a browser/static fallback if npm/Electron install or launch fails.

## v1.1.0 - Native app holster and Omnibinary runtime boundary

- Added `ai-meter app` for one-command native GUI launch.
- Added `native/launcher`, an Electron-based cross-system desktop holster.
- Kept `ai-meter runtime` as the no-GUI/headless path.
- Made `ai-meter gui` fall back to the app holster when Tkinter is unavailable.
- Bundled the uploaded Omnibinary Runtime handoff under `integrations/omnibinary-runtime`.
- Extended the Omnibinary provider to detect `PRODUCT_STATUS.json` while still showing No active Muse until a real model/Muse connection exists.

## v1.0.8 - One-command GUI/runtime launcher

- Added `ai-meter gui` to launch the no-server GUI and background runtime writer in one command.
- Added `ai-meter runtime` for no-GUI/headless operation.
- Added packaged Tk native GUI module under `ai_meter.gui` so Catalina users do not need Tauri/WebKit.
- Preserved `No active Muse` / `No Muse.` disconnected state.

## v1.0.7 — SVG No Muse Label Fix

- Updated the actual SVG buddy label to say `No Muse.` when no active Muse/model payload is connected.
- Removed the periodless `No Muse` disconnected label from the native inline SVG and packaged SVG asset.
- Preserved the main disconnected header as `No active Muse` and active status as `✶ Musing...`.

## v1.0.6 — Correct Muse Connection and Eye Blink Behavior

- Browser/Vite preview now defaults to `No active Muse` instead of loading a fake active browser sample.
- Removed the fake black blink overlay.
- Blinking now only hides the two yellow eye pixels.
- Blink timing now runs at randomized 3–11 second intervals only when not musing.
- Catalina fallback follows the same connection and blink rules.

# Changelog

## v1.0.4 — No Active Muse Disconnected State

- Added explicit `No active Muse` UI state for missing, invalid, offline, planned, or disconnected payloads.
- Updated native Tauri frontend fallback behavior so disconnected state does not display `Musing...`.
- Updated Catalina fallback app to show `No active Muse` when not connected.
- Preserved animated `✶ Musing...` only for active/connected payloads.

## v1.0.3 — Animated Musing State and Runtime Action Layer

- Added animated Musing dots and blinking buddy eye overlay in the native frontend.
- Added last action, action in progress, CLI checker, and run log fields to status payloads.
- Added `ai-meter check-cli` for CLI checker probes.
- Added browser-safe fallback and JSON import path so Vite preview does not crash outside Tauri.
- Added Tauri icon asset required for native launch/build.
- Kept no-local-server default: file/stdout/serial payload flow remains primary.


## 1.0.2

- Added a real Tauri/Rust native desktop app under `native/tauri`.
- Native app reads `runtime/status.json` directly through a Rust command; no local server is required.
- Added native frontend files, Rust backend command, Tauri config, package manifest, and release notes.
- Preserved the exact orange/blue pixel buddy SVG and `✶ Musing...` baseline state in the native shell.
- Kept the localhost API as optional development/debug tooling only.

## 1.0.1

- Added no-server default runtime commands: `write-status`, `write-companion`, `watch`, and `watch-companion`.
- Added atomic JSON file writer for full dashboard and compact companion payloads.
- Added dashboard file-import workflow so `docs/index.html` can render payloads without a local HTTP server.
- Reframed the HTTP API as optional development/debug preview tooling only.
- Added `docs/no-local-server-default.md` and release notes for v1.0.1.

# Changelog

## v1.0.4 — No Active Muse Disconnected State

- Added explicit `No active Muse` UI state for missing, invalid, offline, planned, or disconnected payloads.
- Updated native Tauri frontend fallback behavior so disconnected state does not display `Musing...`.
- Updated Catalina fallback app to show `No active Muse` when not connected.
- Preserved animated `✶ Musing...` only for active/connected payloads.

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


## v1.1.7 — Specs Visibility + Muse State Polish

- Added DIY / Cost Specs panel to the runtime dashboard page.
- Added direct links from the runtime docs panel to the DIY hardware spec and BOM/cost section.
- Added docs-page section for DIY/cost specs and a back-to-runtime-dashboard link.
- Clarified red/green connection dot semantics: runtime connected only, not Muse active.
- Preserved No active Muse for mock/runtime-only states.
- Tightened SVG eye-only blink behavior and made first idle blink occur within 3 seconds for visible verification.
