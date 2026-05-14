# AI Desk Meter v1.1.5 — Runtime Dashboard Button

- Added a Dashboard button to the runtime page.
- In the Electron holster, Dashboard starts/opens the lightweight browser runtime dashboard at `http://127.0.0.1:1420/#muse`.
- In the external browser/Vite page, Dashboard returns to the same live runtime dashboard page.
- Docs now opens the docs site/page instead of the same runtime panel.
- The runtime dashboard keeps listening to `runtime/status.json` as the lightweight source of truth and updates the red/green connection dot automatically.
