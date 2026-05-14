# AI Desk Meter v1.2.1 — Runtime Dashboard IP Server Fix

This release fixes the Dashboard button/runtime IP page connection problem.

## Changes

- Electron holster now starts a built-in lightweight HTTP runtime dashboard server on `127.0.0.1:1420`.
- The runtime dashboard IP page no longer depends on Vite being installed or running.
- `/runtime/status.json` is served directly from the active source-of-truth payload path.
- `/health` reports whether the dashboard IP site is alive and whether the runtime payload exists.
- Dashboard button opens `http://127.0.0.1:1420/#muse`.
- Electron app and external browser dashboard stay in sync from the same `runtime/status.json`.
- Runtime connected still means CLI/runtime/dashboard reachable, not Muse connected.

## Expected behavior

`ai-meter app` starts the runtime writer, starts the app holster, starts the dashboard IP site, and opens the local runtime dashboard without needing a manual Vite process.
