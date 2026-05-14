# Arduino Serial Companion Firmware

This example reads one compact companion JSON payload per serial line and renders the key status to Serial. It is intended for UNO/Nano/Mega-style experiments or as a starting point for tiny OLED/LCD displays.

Send a minified payload like:

```text
{"schema":"ai_desk_meter_companion_v1","status":"linked","current_pct":50,"weekly_pct":11,"current_reset":"1h 22m","weekly_reset":"6d 8h","activity":"musing","message":"✶ Musing...","warnings":0,"errors":0}
```
