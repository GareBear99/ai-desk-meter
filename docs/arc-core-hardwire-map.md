# ARC-Core Hardwire Map

Status: v0.9 boundary map.

This document defines how AI Desk Meter should understand the wider ARC system without taking authority from it.

## Authority separation

| Layer | Responsibility |
|---|---|
| ARC-Core | canonical authority, cases, receipts, state decisions, validation rules |
| Arc-RAR | portable archive bundles, receipt packaging, cross-system restore, integrity checks |
| Omnibinary | binary event spine, replay ledger, event-state reconstruction |
| AI Desk Meter | dashboard, provider health, compact display payloads, diagnostics |
| Neural Synth | later visualization mode driven by real provider state |
| MuseMeter 3.0 | later commercial full package / second-brain AI buddy direction |

## Hardwire principle

AI Desk Meter should be able to attach to any supported system through documented providers while keeping the source of truth outside the UI.

The canonical state flow is:

```text
ARC-Core authority
  -> receipts / validated state
  -> Arc-RAR portable archive bundle
  -> Omnibinary event spine / replay mirror
  -> AI Desk Meter provider payload
  -> dashboard / companion display / diagnostics
```

## Required dashboard rule

The dashboard may display:

- health
- activity
- warnings
- errors
- latest checkpoint references
- portable/not-portable state
- linked/offline/stale/error modes

The dashboard must not:

- overwrite canonical ARC-Core state
- fabricate Omnibinary events
- claim Neural Synth is live before real provider state exists
- silently ignore provider errors

## Adapter boundary

Every backend connector should pass through the provider contract in `docs/provider-contract.md`.

Provider output should remain dashboard-safe:

```text
read-only
small enough for hardware displays
safe for diagnostics export
no secrets or private prompt content by default
```
