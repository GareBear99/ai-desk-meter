# AI Desk Meter v1.0.6 — Correct Muse Connection and Eye Blink Behavior

This release corrects the native/browser preview behavior so the UI no longer pretends a Muse/model is active when only the browser fallback is loaded.

## Changes

- Browser/Vite preview now defaults to **No active Muse** until a real runtime payload is imported or a native payload is read.
- Removed the fake black blink overlay.
- Blinking is now limited to the two yellow eye pixels.
- Eye blink hides those two yellow eyes briefly instead of drawing a misplaced black bar.
- Blink timing occurs at randomized 3–11 second intervals when the buddy is not musing.
- When `✶ Musing...` is active, the dots animate, but the idle blink scheduler is disabled.
- Catalina fallback mirrors the same No active Muse and eye-blink rules.

## Product rule

A Muse is considered active only when a valid connected runtime/model payload is present. Otherwise the UI must say **No active Muse**.
