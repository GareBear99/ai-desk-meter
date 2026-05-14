# Dashboard Refresh

The GitHub Pages dashboard can now poll a local AI Desk Meter API when it is opened on the same machine or local kiosk.

Default local endpoint:

```text
http://127.0.0.1:8787/status?provider=mock
```

Provider examples:

```text
http://127.0.0.1:8787/status?provider=arcrar
http://127.0.0.1:8787/status?provider=arcrar-cli
```

The dashboard must treat provider data as display state only. Backend truth remains inside the provider/backend layer.

Expected states:

- `active` — provider is linked and returning usable state
- `offline` — provider/backend is missing or unavailable
- `stale` — state exists but is old
- `error` — provider returned invalid or failed output
- `demo` — mock/demo state

The dashboard should never invent receipt/archive state. If Arc-RAR is unavailable, show the offline payload.
