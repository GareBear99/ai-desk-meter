# Test Matrix

## Host provider tests

| Case | Expected result |
|---|---|
| Mock provider | Valid active payload with mock confidence |
| Manual provider | Valid active payload with estimated confidence |
| Arc-RAR state file valid | Valid active payload with backend metadata |
| Arc-RAR state file missing | Offline payload, unknown confidence, warning present |
| Arc-RAR state file corrupt | Error payload, unknown confidence, warning/error present |
| Invalid percentage values | Validation rejects or clamps through model rules |

## Transport tests

| Case | Expected result |
|---|---|
| Stdout transport | Emits one compact JSON object |
| Wi-Fi endpoint unavailable | Raises controlled transport error |
| Single-shot mode | Exits after one payload |
| Poll loop | Sleeps between payloads and handles interruption |

## Device class tests

| Device | Expected capability |
|---|---|
| macOS | Full host daemon and docs workflow |
| Windows | Full host daemon and docs workflow |
| Linux | Full host daemon and docs workflow |
| Raspberry Pi | Full host daemon, kiosk/bridge target |
| ESP32-S3 | JSON display endpoint |
| Arduino-class MCU | Simplified telemetry/display endpoint only |

## Release gate

A release should not be tagged until:

- `python -m pytest` passes in `host/`
- `ai-meter test-payload` prints valid JSON
- `ai-meter start --provider mock --transport stdout --once` works
- `ai-meter start --provider arcrar --transport stdout --once` handles both valid and missing state files
- README and docs match the actual implemented state
