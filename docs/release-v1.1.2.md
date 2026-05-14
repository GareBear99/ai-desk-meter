# AI Desk Meter v1.1.2 — Unified Runtime / Dev Page

v1.1.2 makes the app page and external browser page the same runtime surface.

## Changes

- Integrated Runtime / Connection, Dev JSON, Commands, Providers / Omnibinary, and Logs panels into the main runtime page.
- Electron native holster loads the same page as the browser/Vite preview.
- The browser opened from the app uses the same page with `#dev` rather than a separate generated HTML report.
- Localhost server remains optional dev/debug tooling only.
- No-server JSON payloads remain the default runtime mechanism.

## UX rule

One runtime page. Multiple shells. Same dashboard, same dev info, same JSON view.
