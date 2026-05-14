from __future__ import annotations

import json

from ai_meter.writer import write_status


def test_mock_runtime_connected_but_no_active_muse(tmp_path):
    out = tmp_path / "status.json"
    write_status(out, "mock")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["runtime_connected"] is True
    assert data["muse_connected"] is False
    assert data["muse_state"] == "none"
    assert data["status"] == "No active Muse"
    assert data["cli_checker"]["state"] == "active"
