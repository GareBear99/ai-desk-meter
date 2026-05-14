# Hardware Companion Protocol

AI Desk Meter v0.6 adds a compact, display-safe payload for ESP32 and Arduino-class companion devices.

## Endpoint

```text
GET /companion/status?provider=mock
GET /companion/status?provider=arcrar
GET /companion/status?provider=arcrar-cli
```

The full host, provider validation, Arc-RAR access, diagnostics, and archive authority stay on the desktop or Raspberry Pi/Linux SBC. Microcontrollers only display or forward a compact state.

## Payload

```json
{
  "schema": "ai_desk_meter_companion_v1",
  "status": "linked",
  "current_pct": 50,
  "weekly_pct": 11,
  "current_reset": "1h 22m",
  "weekly_reset": "6d 8h",
  "activity": "musing",
  "message": "✶ Musing...",
  "burn_rate": "normal",
  "backend": "arcrar-cli",
  "receipt_state": "available",
  "archive_state": "verified",
  "hardwire_state": "portable",
  "warnings": 0,
  "errors": 0
}
```

## Activity states

`musing` is the intentional baseline state while an agent is responding to prompt input or an action is loading. Later versions can split this into `responding`, `loading`, `tool`, or `idle` without changing the v1 display contract.

## Companion device rules

- Accept unknown fields and ignore them.
- Render errors and offline states clearly.
- Do not store secrets, prompts, tokens, or private AI content.
- Do not treat the companion device as the source of truth.
- Prefer short polling intervals of 0.5-10 seconds.
