# Omnibinary Runtime Holster Integration

This package includes the uploaded Omnibinary Runtime handoff under `integrations/omnibinary-runtime`.

AI Desk Meter does **not** claim that Omnibinary is a finished universal runtime. The bundled Omnibinary package identifies itself as a production-track runtime foundation with the universal runtime core not yet production ready.

## Provider behavior

The `omnibinary` provider now supports:

- `AI_METER_OMNIBINARY_STATE=/path/to/state.json` for explicit adapter fixtures.
- `AI_METER_OMNIBINARY_REPO=/path/to/omnibinary-runtime` for repo status detection.
- bundled `integrations/omnibinary-runtime/PRODUCT_STATUS.json` detection.

Until an actual Muse/model runtime connection exists, the GUI must still show **No active Muse**.

## Role in the roadmap

Omnibinary is treated as the future binary event spine / replay substrate. The native holster surfaces its readiness and blocker state without pretending it is already an active Muse.
