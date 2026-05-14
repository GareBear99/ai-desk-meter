# Release Checklist

Before tagging a release:

- [ ] README describes only implemented behavior and clearly marks roadmap items.
- [ ] `cd host && python -m pytest` passes.
- [ ] `ai-meter test-payload` prints valid JSON.
- [ ] `ai-meter providers` lists `arcrar`, `arcrar-cli`, `manual`, and `mock`.
- [ ] `AI_METER_ARCRAR_STATE=../examples/arcrar_meter_state.example.json ai-meter start --provider arcrar --transport stdout --once` returns an active payload.
- [ ] Missing Arc-RAR state returns an offline payload.
- [ ] Corrupt Arc-RAR state returns an error payload.
- [ ] Missing Arc-RAR CLI executable returns an offline payload.
- [ ] Invalid Arc-RAR CLI JSON returns an error payload.
- [ ] Arc-RAR CLI timeout returns an error payload.
- [ ] Docs mention Raspberry Pi/SBC support accurately.
- [ ] Docs describe Arduino-class boards as endpoints/companions, not full backend hosts.
- [ ] No trademark-risk branding remains in public copy.
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
