# AI Desk Meter Host

Python host daemon for AI Desk Meter.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

```bash
ai-meter test-payload
ai-meter providers
ai-meter start --provider mock --transport stdout --once
ai-meter start --provider mock --transport wifi --url http://192.168.1.44/api/state
```

## Arc-RAR state-file provider

```bash
AI_METER_ARCRAR_STATE=../examples/arcrar_meter_state.example.json   ai-meter start --provider arcrar --transport stdout --once
```

The Arc-RAR provider fails closed when state is missing or invalid.
