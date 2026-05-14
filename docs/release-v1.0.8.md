# AI Desk Meter v1.0.8 — One-command GUI/runtime launcher

This release adds a one-command no-server desktop launcher.

## New commands

```bash
ai-meter gui
ai-meter runtime
```

`ai-meter gui` opens the local GUI and automatically starts the background JSON runtime writer. No localhost API, no browser setup, and no separate watcher terminal are required.

`ai-meter runtime` keeps the no-GUI payload flow for headless devices, Raspberry Pi, scripts, and companion displays.

## Modes

- GUI mode: `ai-meter gui --provider mock`
- No-GUI runtime mode: `ai-meter runtime --provider mock --out runtime/status.json --interval 0.5`
- GUI-only display mode: `ai-meter gui --no-runtime --out runtime/status.json`

The GUI still uses `No active Muse` / `No Muse.` until a valid Muse/model payload is connected.
