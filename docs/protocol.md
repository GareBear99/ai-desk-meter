# Protocol

The meter protocol is one JSON object representing the latest display state.

## Current schema

```json
{
  "schema": "ai-desk-meter.v1",
  "service": "claude-code",
  "current_percent": 50,
  "weekly_percent": 11,
  "current_reset_seconds": 4920,
  "weekly_reset_seconds": 547200,
  "burn_rate": "normal",
  "status": "Musing...",
  "mode": "active",
  "updated_at": 1760000000,
  "source": "mock",
  "confidence": "mock"
}
```

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

- Clamp percentage values between 0 and 100.
- Reject payloads with missing schema.
- Treat stale payloads as stale after 90 seconds.
- Treat no payload for 5 minutes as offline.
- Never display hidden assumptions as exact usage.
