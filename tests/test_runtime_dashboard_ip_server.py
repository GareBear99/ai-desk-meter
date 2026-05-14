from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_electron_holster_serves_runtime_dashboard_ip_site_without_vite():
    main = (ROOT / "native/launcher/main.js").read_text(encoding="utf-8")
    assert "http.createServer" in main
    assert "serveRuntimeDashboardRequest" in main
    assert "'/runtime/status.json'" in main or '"/runtime/status.json"' in main
    assert "'/health'" in main or '"/health"' in main
    assert "npm", "sanity"
    # Runtime dashboard IP site must no longer depend on spawning Vite from the Electron holster.
    assert "npm', ['run', 'dev']" not in main


def test_runtime_dashboard_button_targets_ip_site():
    renderer = (ROOT / "native/launcher/app/renderer.js").read_text(encoding="utf-8")
    main = (ROOT / "native/launcher/main.js").read_text(encoding="utf-8")
    assert "http://127.0.0.1:1420/#muse" in renderer
    assert "DASHBOARD_PORT" in main
    assert "open-runtime-dashboard" in main
