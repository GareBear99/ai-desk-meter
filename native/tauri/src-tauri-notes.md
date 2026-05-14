# src-tauri Implementation Notes

A future committed Tauri app should keep the host process supervised and observable.

## Process supervision options

- Development: run `ai-meter serve` manually or via `beforeDevCommand`.
- Prototype: use a Tauri sidecar to launch the Python host.
- Release: bundle a frozen host executable or require Python installation depending on target audience.

## Required checks

Before loading the dashboard, the shell should check `/health`. If unavailable, it should show a local offline page with setup instructions rather than a blank window.

## Commands to avoid until later

- No direct Omnibinary writes.
- No direct Arc-RAR private internals.
- No hidden LAN binding.
- No account automation or usage-limit bypass behavior.
