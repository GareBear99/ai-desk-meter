# Install and Run

AI Desk Meter v1.0 is a local-first Python host with a browser dashboard and compact hardware companion protocol.

## Desktop / laptop

```bash
cd host
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ai-meter version
ai-meter providers
ai-meter doctor --provider mock
ai-meter serve --host 127.0.0.1 --port 8787
```

Open `docs/index.html` and point the live panel to `http://127.0.0.1:8787`.

## Raspberry Pi / Linux SBC

```bash
chmod +x scripts/install_linux_sbc.sh scripts/run_smoke_test.sh
./scripts/install_linux_sbc.sh
./scripts/run_smoke_test.sh
```

Use the systemd template in `deploy/systemd/` after local smoke tests pass. Keep the API bound to `127.0.0.1` unless you intentionally expose it on a trusted LAN.

## Arc-RAR bridge

Development fixture:

```bash
cd host
AI_METER_ARCRAR_STATE=../examples/arcrar_meter_state.example.json ai-meter status --provider arcrar
```

CLI boundary:

```bash
AI_METER_ARCRAR_BIN=/path/to/arc-rar ai-meter status --provider arcrar-cli
```

If Arc-RAR is not installed, the CLI provider returns an offline payload instead of crashing.
