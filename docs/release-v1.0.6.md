# AI Desk Meter v1.0.6 — Native SVG Eye Blink and Faster Runtime Refresh

v1.0.6 removes the overlay/fake-eye blink implementation from the native frontend. The native UI now inlines the pixel buddy SVG and toggles the actual two SVG eye pixels directly.

## Changes

- Removed the separate `.buddy-eye` DOM overlays entirely.
- Added explicit `muse-eye` elements inside the SVG itself.
- Blink behavior now hides only the actual two SVG eye pixels.
- No blinking occurs while `Musing...` is active.
- Idle blink timing remains randomized from 3–11 seconds.
- Browser/Vite preview no longer overwrites an imported real payload every refresh.
- Frontend refresh cadence reduced from 2 seconds to 0.5 seconds.
- CLI watch default changed to 0.5 seconds and minimum interval lowered to 0.1 seconds.

## Test

```bash
pytest -q
ai-meter version
ai-meter watch --provider mock --out runtime/status.json --interval 0.5
cd native/tauri && npm run dev
```
