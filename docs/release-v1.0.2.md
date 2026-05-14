# AI Desk Meter v1.0.2 — Native Tauri App

v1.0.2 adds the first real native desktop shell.

## Highlights

- Adds a runnable Tauri/Rust desktop app under `native/tauri`.
- Reads `runtime/status.json` directly; no local server required.
- Preserves the orange/blue pixel buddy and `✶ Musing...` state.
- Adds Rust commands for reading and validating the local JSON payload.
- Keeps the localhost API as optional development/debug tooling only.

## Test flow

```bash
source host/.venv/bin/activate
ai-meter watch --provider mock --out runtime/status.json --interval 0.5
```

In a second terminal:

```bash
cd native/tauri
npm install
npm run tauri:dev
```
