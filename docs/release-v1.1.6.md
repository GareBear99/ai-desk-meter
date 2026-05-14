# AI Desk Meter v1.1.6 — Runtime Connection vs Muse State

This patch separates runtime connectivity from Muse/model connectivity.

- Top-right green/red dot now means the CLI/runtime writer and runtime dashboard IP page are reachable.
- `No active Muse` remains visible until a real Muse/model/agent payload is connected.
- Mock/runtime payloads can make the connection dot green without claiming an active Muse.
- Eye blink uses only the real SVG eye pixels.
- Runtime connected + no Muse: random 3–11 second idle blink.
- Muse connected/musing: blink interval is usage-aware: 3s at higher usage, 2s at medium usage, 1s at lower usage.
- The runtime dashboard IP page continues to auto-refresh `runtime/status.json` every 0.5s and mirrors that source of truth.
