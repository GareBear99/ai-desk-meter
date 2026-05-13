# macOS Setup

## Host daemon

```bash
cd host
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
ai-meter test-payload
```

## Firmware tools

```bash
brew install platformio
cd firmware
pio run
```

If PlatformIO is not available through Homebrew on your setup, install it through Python/pipx instead.
