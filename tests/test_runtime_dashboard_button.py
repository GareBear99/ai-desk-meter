from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_dashboard_button_and_docs_routes_are_wired():
    index = (ROOT / "native/launcher/app/index.html").read_text(encoding="utf-8")
    renderer = (ROOT / "native/launcher/app/renderer.js").read_text(encoding="utf-8")
    main = (ROOT / "native/launcher/main.js").read_text(encoding="utf-8")
    vite = (ROOT / "native/tauri/vite.config.js").read_text(encoding="utf-8")
    assert "dashboardButton" in index
    assert "Docs" in index
    assert "openRuntimeDashboard" in renderer
    assert "http://127.0.0.1:1420/#muse" in renderer
    assert "ensureRuntimeDashboardServer" in main
    assert "open-runtime-dashboard" in main
    assert "/docs/index.html" in vite
