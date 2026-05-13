# AI Desk Meter Host

Python host daemon for the ESP32 desk meter.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

```bash
ai-meter test-payload
ai-meter start --provider mock --transport stdout
ai-meter start --provider mock --transport wifi --url http://192.168.1.44/api/state
```
