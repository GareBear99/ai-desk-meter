from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_page_has_connection_dot_and_docs_panel():
    index = (ROOT / 'native/launcher/app/index.html').read_text(encoding='utf-8')
    assert 'connectionPill' in index
    assert 'connectionDot' in index
    assert 'Dashboard' in index
    assert 'Docs' in index
    assert 'docsBackButton' in index
    assert 'runtime/status.json' in index


def test_runtime_page_scripts_autorefresh_source_of_truth():
    renderer = (ROOT / 'native/launcher/app/renderer.js').read_text(encoding='utf-8')
    assert 'setConnectionState' in renderer
    assert 'setInterval(refresh,500)' in renderer or 'setInterval(refresh, 500)' in renderer
    assert 'window.aiDeskMeter.readStatus' in renderer
    assert 'runtime/status.json' in renderer


def test_vite_preview_exposes_runtime_status_json():
    config = (ROOT / 'native/tauri/vite.config.js').read_text(encoding='utf-8')
    assert '/runtime/status.json' in config
    assert 'no-store' in config
    assert 'strictPort' in config


def test_dashboard_button_opens_runtime_dashboard_and_docs_opens_docs_page():
    renderer = (ROOT / 'native/launcher/app/renderer.js').read_text(encoding='utf-8')
    tauri_renderer = (ROOT / 'native/tauri/src/main.js').read_text(encoding='utf-8')
    preload = (ROOT / 'native/launcher/preload.js').read_text(encoding='utf-8')
    main = (ROOT / 'native/launcher/main.js').read_text(encoding='utf-8')
    for source in (renderer, tauri_renderer):
        assert "dashboardButton" in source
        assert "openRuntimeDashboard" in source
        assert "http://127.0.0.1:1420/#muse" in source
        assert "docsButton" in source
        assert "openFullDocsPage" in source
    assert "openRuntimeDashboard" in preload
    assert "open-runtime-dashboard" in main
    assert "devBrowserButton" not in renderer
