# Release Checklist

Before tagging a release:

- [ ] README describes only implemented behavior and clearly marks roadmap items.
- [ ] `cd host && python -m pytest` passes.
- [ ] `ai-meter test-payload` prints valid JSON.
- [ ] `ai-meter providers` lists `arcrar`, `arcrar-cli`, `manual`, `mock`, and `omnibinary`.
- [ ] `AI_METER_ARCRAR_STATE=../examples/arcrar_meter_state.example.json ai-meter start --provider arcrar --transport stdout --once` returns an active payload.
- [ ] Missing Arc-RAR state returns an offline payload.
- [ ] Corrupt Arc-RAR state returns an error payload.
- [ ] Missing Arc-RAR CLI executable returns an offline payload.
- [ ] Invalid Arc-RAR CLI JSON returns an error payload.
- [ ] Arc-RAR CLI timeout returns an error payload.
- [ ] Docs mention Raspberry Pi/SBC support accurately.
- [ ] Docs describe Arduino-class boards as endpoints/companions, not full backend hosts.
- [ ] Public copy uses intentional AI Desk Meter / MuseMeter roadmap wording and avoids accidental legacy branding drift.
- [ ] GitHub Pages renders without broken CSS or old names.

## v0.4 functional checks

- [ ] `ai-meter serve --host 127.0.0.1 --port 8787` starts locally.
- [ ] `/health` returns OK.
- [ ] `/providers` lists mock, manual, arcrar, and arcrar-cli.
- [ ] `/status?provider=mock` returns a valid payload.
- [ ] `/status?provider=arcrar-cli` fails closed if Arc-RAR is missing.
- [ ] Dashboard live panel refreshes from `http://127.0.0.1:8787`.
- [ ] `ai-meter diagnostics --provider mock --out diagnostics.zip` writes a ZIP.
- [ ] Diagnostics bundle contains no secrets, tokens, private prompts, or private AI session content.



## v0.5 hardware/deployment gate

- [ ] `scripts/install_linux_sbc.sh` reviewed and executable
- [ ] `scripts/run_smoke_test.sh` reviewed and executable
- [ ] systemd unit included under `deploy/systemd/`
- [ ] kiosk notes included under `deploy/kiosk/`
- [ ] Raspberry Pi setup docs included
- [ ] network security docs keep loopback as default
- [ ] companion bridge docs clarify Arduino-class devices are endpoints, not backend authority
- [ ] pixel buddy and `✶ Musing...` state preserved in public dashboard/spec
- [ ] licensing roadmap documents open-source corridor and planned MuseMeter 3.0 commercial package


## v0.6 companion bridge

- [ ] `pytest` passes.
- [ ] `ai-meter companion-status --provider mock` returns compact JSON.
- [ ] `/companion/status?provider=mock` works from the local API.
- [ ] ESP32 companion example has Wi-Fi/URL placeholders only.
- [ ] Arduino serial example reads one JSON payload per line.
- [ ] Public docs clearly say microcontrollers are companion nodes, not backend authority.

## v0.7 Arc-RAR CLI contract

- [ ] `arc-rar status --json` valid fixture maps into a dashboard-safe payload.
- [ ] `arc-rar receipts latest --json` can enrich receipt/checkpoint state.
- [ ] `arc-rar archive verify --json` can enrich archive verification state.
- [ ] `arc-rar session inspect --json` can enrich hardwire/portability state.
- [ ] Optional enrichment failures become warnings, not crashes.
- [ ] Required status failures become offline/error states.
- [ ] `docs/arcrar-cli-contract.md` matches provider behavior.

## v0.8 native shell checks

- [ ] `docs/native-gui-plan.md` is present.
- [ ] `native/tauri/tauri.conf.example.json` remains an example, not a signed release claim.
- [ ] Launch scripts default to `127.0.0.1`.
- [ ] Desktop shell docs state that the GUI is not backend authority.
- [ ] Tests pass with `pytest`.


## v0.9 Omnibinary boundary checks

- [ ] `ai-meter status --provider omnibinary` fails closed without state.
- [ ] `AI_METER_OMNIBINARY_STATE=examples/omnibinary_event_state.example.json ai-meter status --provider omnibinary` maps fixture state.
- [ ] Docs clearly state Omnibinary is planned/future integration, not a fully wired backend yet.
- [ ] Neural Synth remains a later visualization layer.
- [ ] MuseMeter 3.0 remains documented as the later commercial full package.


## v1.0 stable release checks

- [ ] `ai-meter version` prints `1.0.0`.
- [ ] `ai-meter doctor --provider mock` returns `ok: true`.
- [ ] `scripts/release_smoke_test.sh` passes on a clean checkout.
- [ ] GitHub Actions workflow is present under `.github/workflows/ci.yml`.
- [ ] `docs/release-v1.0.0.md` clearly separates implemented behavior from future roadmap items.
- [ ] `docs/version-license-matrix.md` preserves the open-source corridor and MuseMeter 3.0 commercial path.
- [ ] `docs/open-source-boundary.md` preserves the intentional pixel buddy and `✶ Musing...` state.
