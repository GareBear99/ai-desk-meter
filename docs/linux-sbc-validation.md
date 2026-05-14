# Linux SBC Validation Checklist

Use this checklist before calling a Raspberry Pi or Linux SBC build validated.

## Baseline

- [ ] Python 3.10+ is installed
- [ ] `scripts/install_linux_sbc.sh` completes
- [ ] `ai-meter providers` lists `mock`, `manual`, `arcrar`, and `arcrar-cli`
- [ ] `ai-meter status --provider mock` prints valid JSON
- [ ] `ai-meter diagnostics --provider mock --out /tmp/diag.zip` creates a non-empty ZIP
- [ ] `ai-meter serve --host 127.0.0.1 --port 8787` starts
- [ ] `/health` returns `ok: true`
- [ ] `/status?provider=mock` returns `ai-desk-meter.v1`

## Arc-RAR paths

- [ ] Missing `arc-rar` executable returns a safe offline/error state
- [ ] State-file provider works with `examples/arcrar_meter_state.example.json`
- [ ] CLI provider works only when `arc-rar status --json` is present and returns valid JSON
- [ ] CLI timeout is bounded by `AI_METER_ARCRAR_TIMEOUT`

## Dashboard

- [ ] Dashboard opens in Chromium/Firefox
- [ ] Live API URL can be set to `http://127.0.0.1:8787`
- [ ] Offline API state is visible and honest
- [ ] Provider warnings/errors are visible
- [ ] The pixel buddy retains the intended “Musing...” loading/responding state

## Hardware notes

- [ ] Pi CPU/memory usage is acceptable during idle dashboard refresh
- [ ] LAN binding is disabled unless specifically required
- [ ] Companion display nodes are treated as render/telemetry endpoints only
