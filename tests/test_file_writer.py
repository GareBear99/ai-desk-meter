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
    assert data["status"] == "✶ Musing..."


def test_write_companion_creates_compact_payload(tmp_path):
    out = tmp_path / "runtime" / "companion.json"
    write_companion(out, "mock")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema"] == "ai_desk_meter_companion_v1"
    assert data["activity"] == "musing"
    assert data["message"] == "✶ Musing..."


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
