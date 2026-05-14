# Protocol

The meter protocol is one JSON object representing the latest display-safe state. It is intentionally small enough for ESP32-class displays while still allowing backend metadata for desktop and Raspberry Pi dashboards.

## Current schema

```json
{
  "schema": "ai-desk-meter.v1",
  "service": "arc-rar",
  "current_percent": 12,
  "weekly_percent": 4,
  "current_reset_seconds": 3600,
  "weekly_reset_seconds": 604800,
  "burn_rate": "low",
  "status": "Arc-RAR linked",
  "mode": "active",
  "updated_at": 1760000000,
  "source": "arcrar",
  "confidence": "estimated",
  "backend": {
    "name": "Arc-RAR",
    "receipt_state": "available",
    "archive_state": "verified",
    "hardwire_state": "portable",
    "checkpoint_id": "local-checkpoint-001"
  },
  "warnings": [],
  "errors": []
}
```

## Required fields

- `schema`
- `service`
- `current_percent`
- `weekly_percent`
- `current_reset_seconds`
- `weekly_reset_seconds`
- `burn_rate`
- `status`
- `mode`
- `updated_at`
- `source`
- `confidence`

## Optional fields

- `backend`
- `warnings`
- `errors`

Small microcontroller clients may ignore optional fields and render only the compact meter state.

## Enums

### burn_rate

- `idle`
- `low`
- `normal`
- `high`
- `critical`

### mode

- `boot`
- `pairing`
- `active`
- `stale`
- `offline`
- `error`
- `demo`

### confidence

- `exact`
- `estimated`
- `mock`
- `unknown`

## Validation rules

- Percent values must remain between 0 and 100.
- Reset timers must be non-negative integers.
- Status text is capped to device-safe length.
- Stale payloads should be marked stale after 90 seconds by clients.
- No payload for 5 minutes should become offline on clients.
- Never display hidden assumptions as exact usage.
- Missing/corrupt backend state must become offline/error state.
