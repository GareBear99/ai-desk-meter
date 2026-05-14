# Arc-RAR CLI Contract

AI Desk Meter integrates with Arc-RAR through a process boundary, not by importing Arc-RAR internals. This keeps the dashboard portable across desktop, Raspberry Pi/Linux SBC, and future ARC systems.

## Required command

```bash
arc-rar status --json
```

This command is required. If it is missing, times out, exits non-zero, or returns invalid JSON, AI Desk Meter returns a safe `offline` or `error` payload instead of crashing.

Minimum accepted shape:

```json
{
  "status": "Arc-RAR CLI linked",
  "mode": "active",
  "usage": {
    "current": 50,
    "weekly": 11,
    "current_reset": 4920,
    "weekly_reset": 547200,
    "burn_rate": "normal"
  },
  "arc": {
    "name": "Arc-RAR",
    "receipt_state": "available",
    "archive_state": "verified",
    "hardwire_state": "portable"
  },
  "warnings": [],
  "errors": []
}
```

## Enrichment commands

These commands enrich the dashboard payload. If one fails, the provider preserves the status payload and adds a warning.

```bash
arc-rar receipts latest --json
arc-rar archive verify --json
arc-rar session inspect --json
```

Accepted receipt shape:

```json
{
  "id": "rcpt_2026_05_14_0001",
  "state": "available",
  "checkpoint_id": "chk_2026_05_14_0001"
}
```

Accepted archive verify shape:

```json
{
  "verified": true,
  "state": "verified"
}
```

Accepted session inspect shape:

```json
{
  "session_id": "session_local_0001",
  "portable": true,
  "hardwire_state": "portable"
}
```

## Provider behavior

| Condition | Dashboard result |
|---|---|
| Arc-RAR executable missing | `mode=offline`, warning message |
| `status --json` timeout | `mode=error`, timeout error |
| `status --json` invalid JSON | `mode=error`, invalid-output error |
| `status --json` valid | `mode=active`, linked payload |
| optional receipt/archive/session command fails | linked payload with warning |
| archive verify reports `verified=false` | linked payload with archive error |

## Environment variables

```bash
AI_METER_ARCRAR_BIN=/path/to/arc-rar
AI_METER_ARCRAR_TIMEOUT=3
```

## Design rule

The dashboard reports only what the backend provides. It does not invent receipt state, archive state, portability, or usage measurements.
