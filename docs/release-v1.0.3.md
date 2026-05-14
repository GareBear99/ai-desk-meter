# AI Desk Meter v1.0.3 — Animated Musing State and Runtime Action Layer

v1.0.3 improves the desktop/native dashboard behavior while preserving the no-server default.

## Added

- Animated `✶ Musing...` status dots.
- Blinking pixel buddy eye overlay while the app is in the Musing state.
- Runtime action fields in the full JSON payload:
  - `last_action`
  - `action_in_progress`
  - `cli_checker`
  - `run_log`
- Native GUI panels for:
  - Last action
  - Action in progress
  - CLI checker state
  - Runtime source
  - Run log
- Browser-safe fallback so Vite preview does not crash when Tauri `invoke` is unavailable.
- JSON import button for local browser-preview testing.
- `ai-meter check-cli` command.
- Tauri icon asset required by native dev/build.

## Default runtime rule

AI Desk Meter still does not require a local server. The primary runtime path remains:

```text
provider/backend -> runtime/status.json -> GUI/device
```

The optional localhost API remains only for development/debug preview workflows.

## Catalina note

Tauri v2 may still be incompatible with macOS Catalina WebKit on some systems. The frontend preview and no-server file payloads are validated; a Catalina-specific native fallback remains the safest path for macOS 10.15 if the Tauri WebKit layer panics at runtime.
