# Test Matrix

## Host provider tests

| Case | Expected result |
|---|---|
| Mock provider | Valid active payload with mock confidence |
| Manual provider | Valid active payload with estimated confidence |
| Arc-RAR state file valid | Valid active payload with backend metadata |
| Arc-RAR state file missing | Offline payload, unknown confidence, warning present |
| Arc-RAR state file corrupt | Error payload, unknown confidence, warning/error present |
| Arc-RAR CLI executable missing | Offline payload, unknown confidence, warning present |
| Arc-RAR CLI valid JSON | Active payload with backend metadata |
| Arc-RAR CLI invalid JSON | Error payload, unknown confidence, error present |
| Arc-RAR CLI non-zero exit | Error payload, unknown confidence, error present |
| Arc-RAR CLI timeout | Error payload, unknown confidence, timeout error present |
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
- `ai-meter status --provider arcrar-cli` fails closed when Arc-RAR is not installed
- README and docs match the actual implemented state


## Raspberry Pi / Linux SBC deployment

- `scripts/install_linux_sbc.sh` completes on Python 3.10+
- `scripts/run_smoke_test.sh` passes after install
- systemd unit starts with loopback binding
- dashboard can poll `http://127.0.0.1:8787/status?provider=mock`
- diagnostics ZIP export works on target hardware
- missing Arc-RAR returns a safe provider error/offline payload

## Character/state preservation

- dashboard keeps the baseline orange/blue pixel buddy
- default loading/responding language remains `✶ Musing...`
- future state differentiation must preserve the baseline state as a fallback


## v0.6 companion bridge checks

- `ai-meter companion-status --provider mock` returns `ai_desk_meter_companion_v1`.
- `/companion/status?provider=mock` returns compact display-safe JSON.
- Missing/offline providers remain display-safe and do not crash the API.
- ESP32 and Arduino example firmware artifacts are present.
- Companion payload excludes private prompts, tokens, and private session content.
