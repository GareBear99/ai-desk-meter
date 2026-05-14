# Arc-RAR Integration Specification

This document defines the intended Arc-RAR integration path for AI Desk Meter.

## Purpose

Arc-RAR is treated as the portable receipt/archive backend. AI Desk Meter is the local display and control surface that reports Arc-RAR state clearly.

## Phase 1: State-file bridge

The state-file bridge is the current safe adapter. It lets the dashboard and devices be tested before Arc-RAR exposes a stable CLI/API.

Required file:

```text
AI_METER_ARCRAR_STATE=/path/to/arcrar_meter_state.json
```

Minimum fields:

```json
{
  "status": "Arc-RAR linked",
  "mode": "active",
  "backend": {
    "receipt_state": "available",
    "archive_state": "verified",
    "hardwire_state": "portable"
  }
}
```

## Phase 2: CLI/API bridge

The next implementation should add an `arcrar-cli` provider that shells out to stable Arc-RAR commands with timeouts and JSON validation.

Candidate commands:

```text
arc-rar status --json
arc-rar archive verify --json
arc-rar receipts latest --json
arc-rar diagnostics --json
```

Required safety behavior:

- Apply a short timeout
- Validate JSON before display
- Preserve command stderr in diagnostics, not on the device payload
- Return `mode="error"` for corrupt JSON
- Return `mode="offline"` for missing executable/backend

## Phase 3: Cross-system hardwire reports

Once Arc-RAR provides portable hardwire receipts, AI Desk Meter should display:

- Current system profile
- Archive portability status
- Receipt chain health
- Last verified checkpoint
- Restore readiness
- Backend compatibility flags

## Phase 4: Diagnostics export

The dashboard should export a diagnostic bundle containing:

- Last validated payload
- Provider name/version
- Backend command status
- Warnings/errors
- Platform info
- Test matrix result snapshot

No secrets, tokens, private prompts, or proprietary local paths should be included by default.
