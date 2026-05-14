# Tauri Shell

The Tauri shell is implemented under `native/tauri`.

## Files

```text
native/tauri/package.json
native/tauri/index.html
native/tauri/src/main.js
native/tauri/src/styles.css
native/tauri/public/pixel-buddy-musing.svg
native/tauri/src-tauri/Cargo.toml
native/tauri/src-tauri/tauri.conf.json
native/tauri/src-tauri/build.rs
native/tauri/src-tauri/src/main.rs
```

## Commands

```bash
cd native/tauri
npm install
npm run tauri:dev
npm run tauri:build
```

The native shell reads `runtime/status.json` by default and supports `AI_METER_STATUS_PATH` for an absolute override.
