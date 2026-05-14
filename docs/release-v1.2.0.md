# AI Desk Meter v1.2.0 — Stable Runtime App Shell

This release locks the runtime dashboard into a stable app shell. The main fix is separating static navigation/buttons/tabs from live runtime payload painting so the dashboard streams smoothly without button/tab flicker or two-truth state flashes.

## Highlights

- Static buttons, tabs, and layout render once.
- Runtime polling updates only value/text nodes.
- No `innerHTML` rebuild of the status title during refresh.
- Holds last good payload across transient file-read misses.
- Runtime dot still means CLI/runtime/dashboard reachable only.
- No active Muse remains until a real Muse/model/agent payload is present.
- Real SVG eye blink remains tied to the actual SVG eye pixels.
- Launcher and browser runtime page share the same renderer logic.

## Commands

```bash
ai-meter app
ai-meter runtime --provider mock --out runtime/status.json --interval 0.5
```
