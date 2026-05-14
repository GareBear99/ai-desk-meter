# Tauri Shell Plan

Tauri is the preferred native shell direction because it aligns with the local-first, Rust-adjacent Arc-RAR architecture while remaining lighter than Electron.

## First prototype behavior

1. Start or verify the local `ai-meter serve` process.
2. Load the dashboard from local static assets or `http://127.0.0.1:8787`.
3. Poll `/health`, `/providers`, `/status`, `/companion/status`, and `/diagnostics`.
4. Show offline/error states if the host is unavailable.
5. Never write provider truth from the frontend without a backend command path.

## Suggested app layout

```text
native/tauri/
├── README.md
├── tauri.conf.example.json
├── frontend-bridge.md
└── src-tauri-notes.md
```

## Development command flow

```bash
cd host
pip install -e .
ai-meter serve --host 127.0.0.1 --port 8787
```

A later implementation can copy `docs/index.html` into a Tauri frontend directory or load it as a local webview.

## Production rule

The desktop shell should bundle or supervise the host service, but it should not silently bind to the LAN. Loopback is the default. LAN access should be explicit.
