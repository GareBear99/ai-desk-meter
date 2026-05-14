# Network Security Notes

AI Desk Meter is local-first. The local API is designed for loopback use by default.

## Default safe binding

Use this unless you have a reason to expose the API to another machine:

```bash
ai-meter serve --host 127.0.0.1 --port 8787
```

## LAN binding

LAN binding is useful for a Raspberry Pi dashboard or ESP32 display on the same trusted network, but it should be intentional:

```bash
ai-meter serve --host 0.0.0.0 --port 8787
```

Before using LAN mode:

- run it only on a trusted local network
- do not expose the port to the public internet
- do not put private prompts, tokens, API keys, or account secrets in provider payloads
- prefer firewall rules that allow only trusted local device IPs
- keep the provider outputs display-safe

## Payload policy

Provider payloads should contain status and meter data only. Do not include private prompt text, private source code, API keys, cookies, account tokens, or raw AI conversation content.
