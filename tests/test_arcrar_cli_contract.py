import json
import stat
from pathlib import Path

from ai_meter.providers.arcrar_cli import ArcRarCliProvider


def _sh_single_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def _contract_arc_rar(tmp_path: Path, responses: dict[str, object], exit_codes: dict[str, int] | None = None) -> Path:
    exit_codes = exit_codes or {}
    lines = ["#!/bin/sh", "key=\"$*\""]
    for key, code in exit_codes.items():
        if code != 0:
            lines.extend([
                f"if [ \"$key\" = {_sh_single_quote(key)} ]; then",
                "  echo 'simulated command failure' 1>&2",
                f"  exit {int(code)}",
                "fi",
            ])
    for key, value in responses.items():
        lines.append(f"if [ \"$key\" = {_sh_single_quote(key)} ]; then")
        if value == "__SLEEP__":
            lines.append("  sleep 5")
        elif value == "__BAD_JSON__":
            lines.append("  printf '%s' 'not json'")
        else:
            lines.append(f"  printf '%s' {_sh_single_quote(json.dumps(value))}")
        lines.append("  exit 0")
        lines.append("fi")
    lines.extend(["printf '%s' '{}'", "exit 0"])
    script = tmp_path / "arc-rar"
    script.write_text("\n".join(lines) + "\n", encoding="utf-8")
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return script


def test_arcrar_cli_contract_merges_status_receipt_archive_and_session(tmp_path: Path):
    exe = _contract_arc_rar(
        tmp_path,
        {
            "status --json": {
                "status": "Arc-RAR CLI linked",
                "mode": "active",
                "confidence": "estimated",
                "usage": {"current": 44, "weekly": 12, "burn_rate": "normal"},
                "arc": {"name": "Arc-RAR", "receipt_state": "available"},
            },
            "receipts latest --json": {"id": "rcpt_123", "state": "available", "checkpoint_id": "chk_123"},
            "archive verify --json": {"verified": True, "state": "verified"},
            "session inspect --json": {"portable": True, "hardwire_state": "portable"},
        },
    )
    payload = ArcRarCliProvider(executable=str(exe)).read().to_wire()
    assert payload["source"] == "arcrar-cli"
    assert payload["mode"] == "active"
    assert payload["current_percent"] == 44
    assert payload["weekly_percent"] == 12
    assert payload["backend"]["receipt_state"] == "available"
    assert payload["backend"]["archive_state"] == "verified"
    assert payload["backend"]["hardwire_state"] == "portable"
    assert payload["backend"]["checkpoint_id"] == "chk_123"
    assert payload["warnings"] == []
    assert payload["errors"] == []


def test_arcrar_cli_contract_optional_command_failure_becomes_warning(tmp_path: Path):
    exe = _contract_arc_rar(
        tmp_path,
        {
            "status --json": {"mode": "active", "usage": {"current": 8, "weekly": 2}},
            "receipts latest --json": {"id": "rcpt_ok", "state": "available"},
            "archive verify --json": {},
            "session inspect --json": {"portable": True},
        },
        exit_codes={"archive verify --json": 2},
    )
    payload = ArcRarCliProvider(executable=str(exe)).read().to_wire()
    assert payload["mode"] == "active"
    assert payload["warnings"]
    assert "archive verify --json" in payload["warnings"][0]


def test_arcrar_cli_contract_required_invalid_status_is_error(tmp_path: Path):
    exe = _contract_arc_rar(
        tmp_path,
        {
            "status --json": "__BAD_JSON__",
            "receipts latest --json": {"id": "rcpt_ok"},
            "archive verify --json": {"verified": True},
            "session inspect --json": {"portable": True},
        },
    )
    payload = ArcRarCliProvider(executable=str(exe)).read().to_wire()
    assert payload["mode"] == "error"
    assert payload["errors"]


def test_arcrar_cli_contract_archive_failed_adds_error(tmp_path: Path):
    exe = _contract_arc_rar(
        tmp_path,
        {
            "status --json": {"mode": "active"},
            "receipts latest --json": {"id": "rcpt_ok"},
            "archive verify --json": {"verified": False, "state": "failed"},
            "session inspect --json": {"portable": False},
        },
    )
    payload = ArcRarCliProvider(executable=str(exe)).read().to_wire()
    assert payload["mode"] == "active"
    assert payload["backend"]["archive_state"] == "failed"
    assert payload["backend"]["hardwire_state"] == "not_portable"
    assert payload["errors"]
