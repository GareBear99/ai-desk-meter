from pathlib import Path


def test_runtime_page_holds_last_good_payload_and_prevents_overlap():
    js = Path("native/tauri/src/main.js").read_text(encoding="utf-8")
    assert "lastStablePayload" in js
    assert "transientDisconnectCount" in js
    assert "refreshInFlight" in js
    assert "handleRuntimeUnavailable" in js


def test_native_holster_renderer_has_stable_blink_signature():
    js = Path("native/launcher/app/renderer.js").read_text(encoding="utf-8")
    assert "lastBlinkSignature" in js
    assert "blinkSignatureFor" in js
    assert "signature === lastBlinkSignature" in js
