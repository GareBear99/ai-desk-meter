# ESP32 Display Guide

ESP32-S3 display boards are the primary companion target for the physical desk meter.

Recommended path:

1. Run the host on desktop or Raspberry Pi.
2. Start the local API:

```bash
ai-meter serve --host 0.0.0.0 --port 8787
```

3. Configure the ESP32 sketch with Wi-Fi credentials and the host IP.
4. Poll:

```text
http://<host-ip>:8787/companion/status?provider=mock
```

## Suggested display

The original recommended target remains valid: Waveshare ESP32-S3-Touch-AMOLED-2.16 or a comparable ESP32-S3 display. The exact orange/blue pixel buddy and `✶ Musing...` baseline are part of the public identity of the device.

## Security note

Use loopback on development machines. Bind to `0.0.0.0` only on a trusted LAN or isolated device network. The companion endpoint is display-safe, but the host should still be treated as a local service.
