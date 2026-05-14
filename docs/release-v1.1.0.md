# AI Desk Meter v1.1.0 — Native App Holster + Omnibinary Runtime Boundary

## Highlights

- Adds `ai-meter app` as the packaged native GUI holster launcher.
- Adds `native/launcher`, an Electron-based cross-system app shell.
- Keeps `ai-meter runtime` as the no-GUI/headless mode.
- Keeps the default architecture no-server: runtime writes local JSON; GUI reads local JSON.
- Makes `ai-meter gui` fall back to the native app holster when Tkinter is unavailable.
- Bundles the uploaded Omnibinary Runtime handoff under `integrations/omnibinary-runtime`.
- Extends the Omnibinary provider to detect `PRODUCT_STATUS.json` without claiming a live Muse connection.

## User-facing commands

```bash
ai-meter app
ai-meter runtime --provider mock --out runtime/status.json --interval 0.5
```
