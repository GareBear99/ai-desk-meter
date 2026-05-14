from __future__ import annotations

import zipfile

from ai_meter.diagnostics import build_diagnostics_payload, write_diagnostics_zip


def test_build_diagnostics_payload():
    data = build_diagnostics_payload("mock")
    assert data["schema"] == "ai-desk-meter.diagnostics.v1"
    assert data["provider"] == "mock"
    assert data["payload"]["schema"] == "ai-desk-meter.v1"
    assert "env_flags" in data["environment"]


def test_write_diagnostics_zip(tmp_path):
    out = write_diagnostics_zip(tmp_path / "diag.zip", "mock")
    assert out.exists()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
    assert "payload.json" in names
    assert "diagnostics.json" in names
    assert "README_DIAGNOSTICS.txt" in names
