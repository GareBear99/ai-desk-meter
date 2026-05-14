from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_electron_holster_uses_unified_runtime_page_and_ipc():
    index = (ROOT / "native/launcher/app/index.html").read_text(encoding="utf-8")
    renderer = (ROOT / "native/launcher/app/renderer.js").read_text(encoding="utf-8")
    main = (ROOT / "native/launcher/main.js").read_text(encoding="utf-8")
    preload = (ROOT / "native/launcher/preload.js").read_text(encoding="utf-8")
    assert "Runtime / Connection" in index
    assert "Dev JSON" in index
    assert "Internal CLI commands" in index
    assert "Providers / Omnibinary" in index
    assert "Dashboard" in index
    assert "dev-connection.html" not in main
    assert "open-dev-view" in main
    assert "#docs" in main
    assert "updateDevPanels" in renderer
    assert "setupTabs" in renderer
    assert "openDevView" in preload
    assert "openDocsPage" in preload
    assert "open-docs-page" in main


def test_tauri_browser_page_uses_same_runtime_panels():
    index = (ROOT / "native/tauri/index.html").read_text(encoding="utf-8")
    renderer = (ROOT / "native/tauri/src/main.js").read_text(encoding="utf-8")
    assert "Runtime / Connection" in index
    assert "Dev JSON" in index
    assert "Internal CLI commands" in index
    assert "Providers / Omnibinary" in index
    assert "updateDevPanels" in renderer
    assert "setupTabs" in renderer


def test_app_launcher_has_resilient_browser_fallback():
    launcher = (ROOT / "host/ai_meter/app_launcher.py").read_text(encoding="utf-8")
    assert "_open_browser_fallback" in launcher
    assert "npm install failed" in launcher
    assert "native holster exited" in launcher
