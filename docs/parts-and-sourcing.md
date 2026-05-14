# AI Desk Meter Parts & Sourcing Guide

This page is the build-ready sourcing sheet for the AI Desk Meter hardware path. It is written so a user can buy parts without guessing, while keeping the software/runtime usable with no hardware attached.

## Recommended core display board

| Item | Recommended part | Purpose | Required? | Estimated street price | Search term | Best source | Notes |
|---|---|---:|---:|---:|---|---|---|
| Touch AMOLED ESP32 board | **Waveshare ESP32-S3-Touch-AMOLED-2.16** | Main desk-meter display and Wi-Fi/BLE companion endpoint | Recommended | **About $30 USD direct** before shipping/options | `ESP32-S3-Touch-AMOLED-2.16` | Waveshare official store | 2.16-inch 480×480 capacitive AMOLED, ESP32-S3, Wi-Fi/BLE, microphones, IMU, RTC, audio/power features. |
| USB-C cable | Data-capable USB-C cable | Flashing firmware and/or desk power | Required | $5–$15 | `USB-C data cable short right angle` | Amazon/local electronics | Avoid charge-only cables. |
| USB power | 5V USB adapter or powered computer/SBC port | Runs the desk meter | Required | $0–$15 | `5V USB-C power adapter` | Any reputable vendor | Use a stable supply; do not rely on weak hubs. |
| Enclosure/stand | 3D printed or small desktop stand | Protects board and gives product feel | Optional | $5–$50 | `ESP32-S3 AMOLED 2.16 case` / custom 3D print | Printables/MakerWorld/local print | Current repo includes enclosure notes; final case can be custom. |
| Fasteners | M2/M2.5 screws, heat-set inserts, rubber feet | Cleaner product-style assembly | Optional | $5–$15 | `M2 screw kit heat set inserts rubber feet` | Amazon/electronics/hobby | Only needed for a finished enclosure. |
| Battery option | 3.7V lithium battery option/version if supported | Portable/untethered demo mode | Optional | Board option + battery cost | `ESP32-S3-Touch-AMOLED-2.16 lithium battery` | Waveshare / reputable LiPo vendor | Use safe LiPo handling; USB-powered mode is simpler. |
| Runtime host | Mac/Windows/Linux/Raspberry Pi | Runs `ai-meter` and writes `runtime/status.json` | Required for full software loop | Existing computer or Pi | `Raspberry Pi 4` / `Raspberry Pi 5` | Raspberry Pi approved resellers | ESP32/Arduino-class boards are companion displays, not the source-of-truth backend. |

## Official / reliable source list

| Need | Where to get it | What to search/click | Notes |
|---|---|---|---|
| Main board purchase | Waveshare official product page | `ESP32-S3-Touch-AMOLED-2.16` | Best source for exact SKU/options and official pricing. |
| Board documentation | Waveshare Docs/Wiki | `ESP32-S3-Touch-AMOLED-2.16 docs` | Use for pinout, flashing, firmware, and board setup details. |
| Firmware examples | Waveshare GitHub | `waveshareteam ESP32-S3-Touch-AMOLED-2.16` | Vendor sample program; useful as a low-risk firmware reference. |
| ESP-IDF component | Espressif Component Registry | `waveshare esp32_s3_touch_amoled_2_16` | Useful for ESP-IDF/BSP-based firmware work. |
| Quick retail purchase | Amazon / regional marketplace | `Waveshare ESP32-S3 2.16 AMOLED Touch` | Good for convenience, but verify exact 2.16 model and battery option. |
| Case/stand | Printables, MakerWorld, local 3D print, custom model | `ESP32-S3 AMOLED 2.16 case` | Case availability changes; custom case may be needed. |
| Cable/power | Local electronics/Amazon | `short USB-C data cable`, `right angle USB-C data cable` | Data-capable cable is important for flashing. |

## Cost tiers

| Tier | Estimate | What it includes | Use case |
|---|---:|---|---|
| Cheap prototype | **$25–$60** | ESP32 display board or cheaper ESP32 + small display, USB-C cable, no polished case | Protocol/UI proof, development, demos. |
| Best-match desk build | **$50–$120 all-in** | Waveshare 2.16 AMOLED board, decent cable, simple enclosure/stand, basic finish | Recommended AI Desk Meter build. |
| Product-style one-off | **$90–$160** | Board, polished enclosure, fasteners, rubber feet, cable management, optional battery/power polish | Demo-ready or sellable-feeling unit. |

## Buying checklist

Before ordering, confirm:

- The board name says **ESP32-S3-Touch-AMOLED-2.16**.
- The display is **2.16-inch / 480×480**.
- Touch is included.
- You know whether you are ordering the battery option or non-battery option.
- Your USB-C cable supports **data**, not only charging.
- If building a case, you have dimensions or a test-fit plan.
- You understand that ESP32/Arduino-class devices are display/companion endpoints; the runtime source of truth is the desktop/Pi host writing `runtime/status.json`.

## Substitution rules

Acceptable substitutions:

- Any ESP32-S3 display board can prototype the companion protocol if firmware is adapted.
- A Raspberry Pi with HDMI display can run the full runtime dashboard directly.
- Arduino/ESP32 serial displays can show compact `companion.json` only.

Do not claim full compatibility until firmware, display dimensions, and pin mappings are tested.

## Software source of truth

Hardware displays are not the authority. The runtime source of truth remains:

```bash
ai-meter runtime --provider mock --out runtime/status.json --interval 0.5
```

The GUI and companion hardware should mirror that payload. The top-right green dot means runtime/CLI/dashboard reachability. **No active Muse** only changes when a real Muse/model/agent connection exists.
