# Native GUI Plan

AI Desk Meter now includes a real Tauri/Rust native desktop shell under `native/tauri`.

The native app wraps the same product identity as the HTML dashboard but does not require a local HTTP server. It reads the offline-first JSON payload written by the host CLI.

## Default native flow

```text
ai-meter watch --provider mock --out runtime/status.json --interval 0.5
        ↓
native/tauri Rust command reads runtime/status.json
        ↓
Tauri window refreshes usage, weekly usage, reset timers, burn rate, provider, warnings, errors, and ✶ Musing... state
```

## Native app rules

- The GUI is not the backend authority.
- The GUI reads provider payloads; it does not invent usage state.
- No local API/server is required for normal operation.
- The optional `serve` command remains development/debug tooling only.
- MuseMeter 3.0 remains the later commercial second-brain / Neural Synth / AI buddy package.
