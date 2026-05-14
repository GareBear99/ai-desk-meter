# AI Desk Meter v1.1.9 — Smooth Runtime Stream

This release fixes dashboard truth flicker and makes the runtime page stream smoothly.

## Changes

- Runtime dashboard no longer flips between disconnected and connected during a transient file read.
- Last good runtime payload is held briefly while the writer updates `runtime/status.json`.
- Refreshes are guarded so overlapping reads cannot paint two states at once.
- Eye blink timers no longer reset on every 0.5s refresh.
- Real SVG eye blink now remains observable while runtime is connected and no Muse is active.
- Bar transitions were smoothed for low-weight streaming.
- Runtime connected remains separate from Muse connected.

## Rule

Green dot = runtime/CLI/IP dashboard reachable.

`No active Muse` remains until a real agent/Muse payload reports `muse_connected`, `agent_connected`, `active_muse`, or an active `muse_state`.
