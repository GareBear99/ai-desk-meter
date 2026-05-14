# AI Desk Meter v1.1.4 — Runtime Docs Button Fix

This release fixes the unified runtime page controls.

- `Docs / Runtime Info` now opens the integrated docs/runtime panel inside the same page in both the Electron holster and the external browser/Vite page.
- `Back to Muse` returns to the Muse dashboard panel.
- The runtime page no longer depends on the removed `devBrowserButton` element.
- Added an optional `Open Full Docs` action that opens the project documentation page when the shell supports it.
- Preserves the low-weight JSON listener model: the UI listens to `runtime/status.json` and mirrors that source of truth.
