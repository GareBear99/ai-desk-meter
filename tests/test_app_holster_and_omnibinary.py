from __future__ import annotations

import json
from pathlib import Path

from ai_meter.cli import build_parser
from ai_meter.providers.omnibinary import OmnibinaryProvider

ROOT = Path(__file__).resolve().parents[1]


def test_app_command_is_registered():
    help_text = build_parser().format_help()
    assert "app" in help_text
    assert "runtime" in help_text


def test_native_launcher_files_exist():
    required = [
        "native/launcher/package.json",
        "native/launcher/main.js",
        "native/launcher/preload.js",
        "native/launcher/app/index.html",
        "native/launcher/app/renderer.js",
        "native/launcher/app/styles.css",
        "docs/native-app-holster.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_native_launcher_is_no_server_file_payload_shell():
    main = (ROOT / "native/launcher/main.js").read_text(encoding="utf-8")
    renderer = (ROOT / "native/launcher/app/renderer.js").read_text(encoding="utf-8")
    assert "runtime/status.json" in main
    assert "read-status" in main
    assert "localhost" not in main.lower()
    assert "No active Muse" in renderer
    assert "No Muse." in (ROOT / "native/launcher/app/index.html").read_text(encoding="utf-8")


def test_omnibinary_runtime_bundle_and_provider_status():
    status = ROOT / "integrations/omnibinary-runtime/PRODUCT_STATUS.json"
    assert status.exists()
    data = json.loads(status.read_text(encoding="utf-8"))
    assert data["product"] == "OmniBinary Runtime"
    payload = OmnibinaryProvider(repo_path=str(status.parent)).read()
    wire = payload.to_wire()
    assert wire["source"] == "omnibinary"
    assert wire["status"] == "No active Muse"
    assert wire["backend"]["name"] == "Omnibinary"
    assert "No active Muse" in " ".join(wire.get("warnings", []))
