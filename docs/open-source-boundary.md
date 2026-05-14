# Open-Source Boundary

AI Desk Meter v1.0 is the open-source foundation for local metering, provider payloads, Arc-RAR bridge work, diagnostics, companion hardware display payloads, and dashboard refresh.

The project should stay honest about implemented behavior:

- The dashboard renders provider-reported state; it is not the source of truth.
- Arc-RAR providers fail closed when the backend is unavailable.
- Omnibinary is documented and stubbed as a future adapter boundary.
- Neural Synth remains a future visualization layer until real backend state exists.
- The pixel buddy and `✶ Musing...` state are intentional product identity. For now, Musing means the agent is responding to prompt input or an action is loading; later versions can split that into more precise states.

MuseMeter 3.0 is the planned commercial full package built from this foundation.
