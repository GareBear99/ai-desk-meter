# AI Desk Meter Native App

This directory contains the real Tauri/Rust desktop shell for AI Desk Meter.

The native app is intentionally **no-server by default**. It reads `runtime/status.json` through a Rust command exposed by Tauri and refreshes the window every two seconds. The optional localhost API remains available only for development/debug previews and is not required by the native app.

## Run locally

From the repo root:

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

## Build desktop bundle

```bash
cd native/tauri
npm install
npm run tauri:build
```

The compiled bundle will be emitted under `native/tauri/src-tauri/target/release/bundle/`.

## Runtime contract

- `runtime/status.json` is the default payload.
- `AI_METER_STATUS_PATH=/absolute/path/status.json` may override the payload path.
- The native app never invents provider state.
- `✶ Musing...` remains the baseline loading/responding/action state.
- The orange/blue pixel buddy is loaded from `public/pixel-buddy-musing.svg`, copied from the canonical repo asset.
