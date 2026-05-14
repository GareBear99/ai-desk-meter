import json
import stat
from pathlib import Path

from ai_meter.providers.arcrar_cli import ArcRarCliProvider


def _fake_arc_rar(tmp_path: Path, body: str, exit_code: int = 0) -> Path:
    script = tmp_path / "arc-rar"
    script.write_text(
        "#!/bin/sh\n"
        f"printf '%s' {json.dumps(body)}\n"
        f"exit {exit_code}\n",
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return script


def test_arcrar_cli_provider_missing_executable_fails_closed():
    payload = ArcRarCliProvider(executable="definitely-not-real-arc-rar-binary").read().to_wire()
    assert payload["source"] == "arcrar-cli"
    assert payload["mode"] == "offline"
    assert payload["warnings"]


def test_arcrar_cli_provider_reads_valid_output(tmp_path: Path):
    exe = _fake_arc_rar(tmp_path, json.dumps({
        "status": "Arc-RAR CLI linked",
        "mode": "active",
        "current_percent": 7,
        "weekly_percent": 2,
        "burn_rate": "low",
        "backend": {
            "name": "Arc-RAR",
            "receipt_state": "available",
            "archive_state": "verified",
            "hardwire_state": "portable",
            "checkpoint_id": "chk_001"
        }
    }))
    payload = ArcRarCliProvider(executable=str(exe), enrich=False).read().to_wire()
    assert payload["source"] == "arcrar-cli"
    assert payload["mode"] == "active"
    assert payload["backend"]["checkpoint_id"] == "chk_001"
    assert payload["backend"]["archive_state"] == "verified"


def test_arcrar_cli_provider_accepts_compact_backend_shape(tmp_path: Path):
    exe = _fake_arc_rar(tmp_path, json.dumps({
        "arc": {
            "receipt_state": "available",
            "archive_state": "verified",
            "hardwire_state": "portable"
        },
        "usage": {
            "current": 5,
            "weekly": 9,
            "burn_rate": "low"
        }
    }))
    payload = ArcRarCliProvider(executable=str(exe), enrich=False).read().to_wire()
    assert payload["mode"] == "active"
    assert payload["current_percent"] == 5
    assert payload["backend"]["hardwire_state"] == "portable"


def test_arcrar_cli_provider_invalid_json_fails_closed(tmp_path: Path):
    exe = _fake_arc_rar(tmp_path, "not json")
    payload = ArcRarCliProvider(executable=str(exe), enrich=False).read().to_wire()
    assert payload["mode"] == "error"
    assert payload["errors"]


def test_arcrar_cli_provider_nonzero_exit_fails_closed(tmp_path: Path):
    exe = _fake_arc_rar(tmp_path, "{}", exit_code=3)
    payload = ArcRarCliProvider(executable=str(exe), enrich=False).read().to_wire()
    assert payload["mode"] == "error"
    assert payload["errors"]


def test_arcrar_cli_provider_timeout_fails_closed(tmp_path: Path):
    script = tmp_path / "arc-rar"
    script.write_text(
        "#!/bin/sh\n"
        "sleep 2\n"
        "printf '{}'\n",
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    payload = ArcRarCliProvider(executable=str(script), timeout_seconds=0.25, enrich=False).read().to_wire()
    assert payload["mode"] == "error"
    assert "timed out" in payload["errors"][0]
