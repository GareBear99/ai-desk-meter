# AI Desk Meter v1.1.8 — Parts & Sourcing Completion

This release tightens the hardware/spec documentation so the DIY path is build-ready instead of just directional.

## Added

- `docs/parts-and-sourcing.md` with a full parts table, sourcing categories, search terms, cost tiers, and buying checklist.
- Runtime dashboard DIY / Cost Specs panel now includes what to buy, where to get it, and exact search terms.
- Docs page now links Parts & Sourcing directly and includes clearer source categories.
- Native Electron holster and browser runtime page both expose the same sourcing/spec panel.

## Clarified

- Recommended board: Waveshare ESP32-S3-Touch-AMOLED-2.16.
- ESP32/Arduino-class boards are companion/display endpoints, not the backend authority.
- Desktop/Raspberry Pi host remains the source-of-truth runtime writer.
- Green connection dot still means runtime/CLI/dashboard reachable, not active Muse.
