# Native App Holster

AI Desk Meter now includes a cross-system native application holster in `native/launcher`.

The holster is an Electron-based desktop shell intended for macOS Catalina, newer macOS, Windows, Linux, and desktop Linux SBC targets. It reads `runtime/status.json` directly through the native filesystem bridge and does not require a localhost API server.

## Commands

```bash
ai-meter app
```

Starts the runtime writer and opens the packaged GUI.

```bash
ai-meter runtime --provider mock --out runtime/status.json --interval 0.5
```

Runs the no-GUI/headless runtime writer only.

## Boundaries

- `ai-meter app` is the preferred packaged GUI path.
- `ai-meter gui` remains a compatibility alias and falls back to the app holster if Tkinter is unavailable.
- `native/tauri` remains a modern Tauri source path for newer WebKit stacks and future packaging work.
- `native/launcher` is the practical cross-system holster.
- No local server is required.
