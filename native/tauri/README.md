# Native Tauri Shell Prototype

This folder documents the v0.8 native dashboard shell path. It is intentionally a prototype scaffold, not a shipped binary.

## Purpose

Wrap the existing AI Desk Meter dashboard and local API in a desktop-friendly shell while keeping provider/backend truth in the Python host and Arc-RAR provider boundary.

## Expected local service

```bash
cd host
pip install -e .
ai-meter serve --host 127.0.0.1 --port 8787
```

The shell should read:

- `http://127.0.0.1:8787/health`
- `http://127.0.0.1:8787/providers`
- `http://127.0.0.1:8787/status?provider=mock`
- `http://127.0.0.1:8787/companion/status?provider=mock`
- `http://127.0.0.1:8787/diagnostics?provider=mock`

## Character identity

The orange/blue pixel buddy and `✶ Musing...` state are intentional. For now, Musing means prompt response or action loading. Later states can distinguish verifying, archiving, idle, warning, and responding.
