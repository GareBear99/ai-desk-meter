# ESP32 Companion Display Firmware

Example Arduino sketch for ESP32/ESP32-S3 boards that polls the AI Desk Meter compact companion endpoint.

Edit these constants in the sketch:

```cpp
const char* WIFI_SSID = "your-wifi";
const char* WIFI_PASS = "your-password";
const char* STATUS_URL = "http://192.168.1.50:8787/companion/status?provider=mock";
```

This example logs to Serial and includes the pixel-buddy bitmap shape as the stable public character reference. Replace the `renderSerial()` function with board-specific OLED/TFT/AMOLED drawing code.
