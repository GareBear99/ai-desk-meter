# Provider Contract

Providers convert a local source of truth into one validated `UsagePayload`.

## Required behavior

A provider must:

- Return a valid `UsagePayload`
- Mark confidence honestly: `exact`, `estimated`, `mock`, or `unknown`
- Use `mode="error"` or `mode="offline"` when state cannot be trusted
- Preserve backend warnings/errors instead of hiding them
- Avoid network scraping or private dashboard scraping
- Avoid claiming exact usage unless the source is exact

## Current providers

| Provider | Purpose | Confidence |
|---|---|---:|
| `mock` | Moving demo values | mock |
| `manual` | Fixed/manual local state | estimated |
| `arcrar` | Reads a local Arc-RAR state JSON file | estimated/unknown depending on state |
| `arcrar-cli` | Calls `arc-rar status --json` through a timeout-safe subprocess boundary | estimated/unknown depending on result |

## Arc-RAR provider input

The current `arcrar` provider reads a JSON file pointed to by `AI_METER_ARCRAR_STATE`, or by the default path `./arcrar_meter_state.json`.

Example:

```json
{
  "service": "arc-rar",
  "current_percent": 12,
  "weekly_percent": 4,
  "current_reset_seconds": 3600,
  "weekly_reset_seconds": 604800,
  "burn_rate": "low",
  "status": "Arc-RAR linked",
  "mode": "active",
  "confidence": "estimated",
  "backend": {
    "name": "Arc-RAR",
    "receipt_state": "available",
    "archive_state": "verified",
    "hardwire_state": "portable"
  },
  "warnings": [],
  "errors": []
}
```

## Fail-closed example

If the Arc-RAR state file is missing, the provider must return an offline/error payload instead of fabricating backend state.

```json
{
  "schema": "ai-desk-meter.v1",
  "service": "arc-rar",
  "current_percent": 0,
  "weekly_percent": 0,
  "current_reset_seconds": 0,
  "weekly_reset_seconds": 0,
  "burn_rate": "idle",
  "status": "Arc-RAR offline",
  "mode": "offline",
  "source": "arcrar",
  "confidence": "unknown",
  "warnings": ["Arc-RAR state file not found"],
  "errors": []
}
```

## Arc-RAR CLI provider boundary

The implemented `arcrar-cli` provider is the preferred live-backend boundary. It starts with: 

```text
arc-rar status --json
```

Future Arc-RAR commands may add richer health and receipt data:

```text
arc-rar status --json
arc-rar receipts latest --json
arc-rar archive verify --json
arc-rar session inspect --json
```

AI Desk Meter should consume those stable outputs rather than importing private internals.


## CLI provider fail-closed rules

`arcrar-cli` must never crash the dashboard or fabricate backend state. It returns:

- `mode="offline"` when the executable is missing or cannot be launched.
- `mode="error"` when Arc-RAR times out, exits non-zero, emits invalid JSON, or emits a payload that fails validation.
- `confidence="unknown"` for all offline/error states.

Supported environment variables:

```text
AI_METER_ARCRAR_BIN=/path/to/arc-rar
AI_METER_ARCRAR_TIMEOUT=3
```
