# AI Desk Meter v1.0.4 — No Active Muse Disconnected State

v1.0.4 clarifies the disconnected state across the native GUI, browser preview, and Catalina fallback.

When the runtime payload is missing, invalid, offline, planned, or otherwise not connected, the UI now says **No active Muse** instead of implying that a Muse is currently running.

## Behavior

- Connected/active payload: `✶ Musing...` with blinking eyes and animated dots.
- Missing or unreadable payload: `No active Muse`.
- Offline/error/planned payload: `No active Muse`.
- Provider label: `not connected`.
- Action in progress: `none`.
- CLI checker: `inactive`.

This keeps the visual language honest while preserving Musing as the active/responding/loading state.
