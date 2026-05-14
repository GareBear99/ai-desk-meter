# Desktop Security Notes

AI Desk Meter is local-first. The desktop shell should keep the same security posture as the CLI and local API.

## Defaults

- Bind to `127.0.0.1` by default.
- Do not expose prompt text, API keys, auth cookies, account identifiers, or private chat logs in diagnostics.
- Do not claim exact usage unless a provider explicitly reports exact usage.
- Keep Arc-RAR and future Omnibinary integration behind provider contracts.

## Desktop shell boundaries

The webview may request status and diagnostics from the local API. It should not directly mutate backend state unless a future backend command endpoint is documented, authenticated, and tested.

## LAN mode

LAN binding is useful for Raspberry Pi kiosks and companion dashboards, but it should be opt-in:

```bash
ai-meter serve --host 0.0.0.0 --port 8787
```

Only use LAN mode on trusted networks.
