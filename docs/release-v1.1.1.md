# AI Desk Meter v1.1.1 — Native Holster Dev Browser View

This release improves the Electron native holster and launcher resilience.

## Added

- Native holster button: **Open browser dev view**.
- Browser-safe `runtime/dev-connection.html` report generated from Electron.
- Connection JSON, app info, runtime file paths, provider boundaries, internal CLI commands, and optional local API routes.
- Launcher fallback when npm/Electron install or launch fails.

## Behavior

`ai-meter app` still starts the runtime writer first. If Electron is available, it opens the native holster. If Electron cannot install or launch, it opens a browser/static fallback instead of crashing with a Python stack trace.

The local API remains optional for dev/debug only. The default app flow remains no-server local JSON.
