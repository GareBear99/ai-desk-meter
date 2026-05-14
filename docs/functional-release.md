# Functional Release Definition

AI Desk Meter reaches functional v1.0 when it can be installed, inspected, served locally, queried by a dashboard, queried by companion hardware, and exported as a safe diagnostics bundle.

## Required checks

```bash
cd host
pip install -e .
ai-meter version
ai-meter providers
ai-meter doctor --provider mock
ai-meter status --provider mock
ai-meter companion-status --provider mock
ai-meter diagnostics --provider mock --out /tmp/ai-desk-meter-diagnostics.zip
ai-meter serve --host 127.0.0.1 --port 8787
```

In another terminal:

```bash
curl http://127.0.0.1:8787/health
curl http://127.0.0.1:8787/providers
curl http://127.0.0.1:8787/status?provider=mock
curl http://127.0.0.1:8787/companion/status?provider=mock
```

## Expected behavior

- Mock provider returns an active payload.
- Arc-RAR providers fail closed when Arc-RAR is unavailable.
- Diagnostics exclude secrets and private AI content.
- API defaults to loopback.
- Companion endpoint returns compact JSON suitable for ESP32/Arduino-class displays.
