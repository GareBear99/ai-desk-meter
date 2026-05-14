# Catalina Native Fallback

`native/catalina/ai_desk_meter_catalina.py` is a no-server desktop fallback for macOS Catalina and other systems where the modern Tauri/WebKit stack is unavailable or unstable.

It reads `runtime/status.json` directly, refreshes every two seconds, shows the Musing state, animated dots, last action, CLI checker, and the run log.

Run from the repo root:

```bash
python3 native/catalina/ai_desk_meter_catalina.py
```

Keep the payload updated in another terminal:

```bash
ai-meter watch --provider mock --out runtime/status.json --interval 0.5
```
