import json
from pathlib import Path

from ai_meter.providers.arcrar import ArcRarProvider


def test_arcrar_provider_reads_valid_state(tmp_path: Path):
    state = tmp_path / "state.json"
    state.write_text(json.dumps({
        "status": "Arc-RAR linked",
        "mode": "active",
        "current_percent": 12,
        "weekly_percent": 4,
        "burn_rate": "low",
        "confidence": "estimated",
        "backend": {
            "name": "Arc-RAR",
            "receipt_state": "available",
            "archive_state": "verified",
            "hardwire_state": "portable"
        }
    }), encoding="utf-8")

    payload = ArcRarProvider(str(state)).read().to_wire()
    assert payload["source"] == "arcrar"
    assert payload["mode"] == "active"
    assert payload["backend"]["archive_state"] == "verified"


def test_arcrar_provider_missing_file_fails_closed(tmp_path: Path):
    payload = ArcRarProvider(str(tmp_path / "missing.json")).read().to_wire()
    assert payload["mode"] == "offline"
    assert payload["confidence"] == "unknown"
    assert payload["warnings"]


def test_arcrar_provider_corrupt_file_fails_closed(tmp_path: Path):
    state = tmp_path / "corrupt.json"
    state.write_text('{"service": "arc-rar",', encoding="utf-8")
    payload = ArcRarProvider(str(state)).read().to_wire()
    assert payload["mode"] == "error"
    assert payload["confidence"] == "unknown"
    assert payload["errors"]
