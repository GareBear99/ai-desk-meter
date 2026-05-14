# Adapter Boundaries

Status: v0.9 system boundary lock.

AI Desk Meter can support many backends, but every backend must be treated as an adapter behind a stable provider contract.

## Existing adapters

| Adapter | Status | Purpose |
|---|---|---|
| `mock` | working | demo/test values |
| `manual` | working | static manual payloads |
| `arcrar` | working bridge | local Arc-RAR-style JSON state file |
| `arcrar-cli` | working contract | Arc-RAR CLI command output |
| `omnibinary` | planned/fails-closed | future binary event spine/replay state |

## Adapter rules

1. Adapters may fail.
2. Failure must become a visible payload, not a crash.
3. Optional enrichment should warn, not destroy the whole dashboard.
4. Required state should fail closed when missing.
5. No adapter may invent backend health.
6. No adapter may send secrets into diagnostics.
7. UI layers do not become authority.

## Extension order

```text
Arc-RAR compatibility first
Omnibinary adapter second
Neural Synth visualization third
MuseMeter 3.0 commercial second-brain package later
```

## Companion display boundary

Raspberry Pi and Linux SBCs can run the host stack. ESP32/Arduino-class systems are companion display/telemetry endpoints unless explicitly upgraded with a real host runtime.
