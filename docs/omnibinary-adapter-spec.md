# Omnibinary Adapter Spec

Status: planned adapter boundary for the v0.9 open-source foundation.

AI Desk Meter does not treat Omnibinary as a finished backend yet. The v0.9 work locks the adapter shape so later implementations can connect without changing the dashboard protocol.

## Role

Omnibinary is planned as the binary event spine and replay/memory ledger for the wider ARC ecosystem.

It is responsible for:

- binary event lineage
- replay state
- state reconstruction hints
- long-term event mirroring
- future second-brain substrate work

It is not responsible for:

- replacing Arc-RAR archive packaging
- becoming the dashboard authority
- inventing usage values
- driving Neural Synth visuals before real state exists

## Provider name

```text
omnibinary
```

The provider is intentionally fails-closed. Without a configured state source it returns an offline/planned payload.

```bash
ai-meter status --provider omnibinary
```

Optional early integration fixture:

```bash
AI_METER_OMNIBINARY_STATE=examples/omnibinary_event_state.example.json ai-meter status --provider omnibinary
```

## Minimal source-state contract

```json
{
  "schema": "omnibinary.adapter_state.v1",
  "linked": true,
  "status": "Omnibinary linked",
  "checkpoint_id": "ob_chk_001",
  "usage": {
    "current": 12,
    "weekly": 3
  },
  "event": {
    "state": "available",
    "last_event_id": "ob_evt_001",
    "checkpoint_id": "ob_chk_001"
  },
  "replay": {
    "state": "ready",
    "last_replay_id": "ob_replay_001"
  },
  "health": {
    "hardwire_state": "portable"
  },
  "warnings": [],
  "errors": []
}
```

## Dashboard projection

The adapter maps the source state into the existing `ai-desk-meter.v1` payload:

| Omnibinary field | AI Desk Meter field |
|---|---|
| `linked` | `mode=active` when true and no errors |
| `usage.current` | `current_percent` |
| `usage.weekly` | `weekly_percent` |
| `event.state` | `backend.receipt_state` |
| `replay.state` | `backend.archive_state` |
| `health.hardwire_state` | `backend.hardwire_state` |
| `checkpoint_id` | `backend.checkpoint_id` |
| `warnings` | `warnings` |
| `errors` | `errors` |

## Failure behavior

The adapter must never pretend Omnibinary is live.

| Condition | Required behavior |
|---|---|
| No Omnibinary state configured | offline/planned payload with warning |
| Missing state file | offline/planned payload with warning |
| Invalid JSON | error payload |
| Explicit errors in state | error mode with errors preserved |
| Linked state with warnings | active mode with warnings preserved |

## Later implementation options

Future Omnibinary integration may use one or more of these sources:

- local JSON state export
- CLI command output
- local socket
- shared event log tailer
- ARC-Core hardwire bridge

The dashboard should not care which transport is used. It only consumes provider output.
