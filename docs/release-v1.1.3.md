# AI Desk Meter v1.1.3 — Connection Dot + Unified Runtime Docs Panel

This release tightens the native holster/runtime page experience.

## Changes

- Adds a red/green connection dot in the top-right corner of the runtime page.
- The runtime page auto-refreshes from the local source-of-truth payload.
- Electron/native holster reads `runtime/status.json` through the preload bridge.
- Browser/Vite preview can read `runtime/status.json` through a lightweight Vite middleware.
- Replaces the old “open same page” button with an integrated Docs / Runtime Info panel.
- Adds a Back to Muse button on the docs panel.
- Documents that `runtime/status.json` is the source of truth for the page state.
- Preserves no-server default mode and optional local API debug mode.

## Runtime rule

The page does not invent connection state. If no valid active payload is available, it shows **No active Muse** and the dot remains red. Once a valid runtime payload is detected, the dot turns green and the UI mirrors the payload status.
