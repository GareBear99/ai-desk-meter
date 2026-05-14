from __future__ import annotations

import json

from ai_meter.cli import main
from ai_meter.writer import watch_writer, write_companion, write_status


def test_write_status_creates_full_payload(tmp_path):
    out = tmp_path / "runtime" / "status.json"
    written = write_status(out, "mock")
    assert written == out
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema"] == "ai-desk-meter.v1"
    assert data["source"] == "mock"
    assert data["status"] == "No active Muse"
    assert data["runtime_connected"] is True
    assert data["muse_connected"] is False
    assert data["last_action"] == "write-status complete"
    assert data["action_in_progress"] == "none"
    assert data["cli_checker"]["state"] == "active"
    assert any("CLI checker" in row for row in data["run_log"])


def test_write_companion_creates_compact_payload(tmp_path):
    out = tmp_path / "runtime" / "companion.json"
    write_companion(out, "mock")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema"] == "ai_desk_meter_companion_v1"
    assert data["activity"] == "runtime"
    assert data["message"] == "No active Muse"


def test_watch_writer_count_stops_for_tests(tmp_path):
    out = tmp_path / "status.json"
    count = watch_writer(path=out, provider_name="mock", interval_seconds=0.25, count=2)
    assert count == 2
    assert json.loads(out.read_text(encoding="utf-8"))["source"] == "mock"


def test_cli_write_status_and_companion(tmp_path, capsys):
    status_out = tmp_path / "status.json"
    companion_out = tmp_path / "companion.json"
    assert main(["write-status", "--provider", "mock", "--out", str(status_out)]) == 0
    assert main(["write-companion", "--provider", "mock", "--out", str(companion_out)]) == 0
    assert status_out.exists()
    assert companion_out.exists()
    captured = capsys.readouterr()
    assert "status.json" in captured.out
    assert "companion.json" in captured.out


def test_cli_check_cli_outputs_action_state(capsys):
    assert main(["check-cli", "--provider", "mock"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["schema"] == "ai-desk-meter.cli-checker.v1"
    assert data["ok"] is True
    assert data["last_action"] == "CLI checker probe complete"
    assert data["action_in_progress"] == "none"
    assert data["cli_checker"]["state"] == "active"
