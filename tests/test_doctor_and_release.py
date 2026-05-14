from __future__ import annotations

import json
from pathlib import Path

from ai_meter import __version__
from ai_meter.cli import main
from ai_meter.doctor import run_doctor


def test_version_is_v1():
    assert __version__ == "1.2.1"


def test_doctor_mock_is_ok():
    report = run_doctor("mock")
    assert report["schema"] == "ai-desk-meter.doctor.v1"
    assert report["ok"] is True
    assert report["provider"] == "mock"


def test_cli_version_outputs_version(capsys):
    assert main(["version"]) == 0
    out = capsys.readouterr().out.strip()
    assert out == "1.2.1"


def test_cli_doctor_outputs_json(capsys):
    assert main(["doctor", "--provider", "mock"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True


def test_v1_release_docs_exist():
    required = [
        "docs/install.md",
        "docs/release-v1.0.1.md",
        "docs/release-v1.0.7.md",
        "docs/release-v1.0.8.md",
        "docs/release-v1.1.0.md",
        "docs/release-v1.1.6.md",
        "docs/release-v1.2.1.md",
        "docs/parts-and-sourcing.md",
        "docs/version-license-matrix.md",
        "docs/open-source-boundary.md",
        "docs/functional-release.md",
        "scripts/release_smoke_test.sh",
        ".github/workflows/ci.yml",
    ]
    for item in required:
        assert Path(item).exists(), item
