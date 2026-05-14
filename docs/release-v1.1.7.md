# AI Desk Meter v1.1.7 — Specs Visibility + Muse State Polish

This release makes the runtime UX clearer:

- The top-right red/green dot means the runtime/CLI/dashboard pipe is reachable.
- Green runtime status does **not** mean a Muse/model/agent is active.
- `No active Muse` remains until a real Muse/agent payload sets `muse_connected`, `agent_connected`, `active_muse`, or an active `muse_state`.
- The app/browser runtime page now exposes the DIY hardware guide and cost/BOM specs directly.
- The real SVG eyes are the only blinking elements; no overlay eyes are used.
- First idle blink occurs within 3 seconds for easy verification, then continues every 3–11 seconds while runtime is connected and no Muse is active.
- Muse-active blink cadence remains usage-aware: high usage ≈ 3s, medium ≈ 2s, low ≈ 1s.
