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

The `arcrar-cli` provider is now implemented as the next live-backend bridge. It shells out to stable Arc-RAR commands with timeouts and JSON validation.

Implemented command:

```text
arc-rar status --json
```

Candidate future commands:

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


## Current CLI provider usage

```bash
cd host
ai-meter status --provider arcrar-cli
ai-meter start --provider arcrar-cli --transport stdout --once
```

The provider can be configured without changing source code:

```bash
AI_METER_ARCRAR_BIN=/path/to/arc-rar AI_METER_ARCRAR_TIMEOUT=3 ai-meter status --provider arcrar-cli
```

The provider accepts either a full AI Desk Meter payload-style JSON object or a compact Arc-RAR status object with `arc` and `usage` sections. In both cases the final display payload is validated through `UsagePayload`.
