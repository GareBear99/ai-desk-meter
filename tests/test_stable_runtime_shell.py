from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_renderer_does_not_rebuild_controls_on_refresh():
    js = (ROOT / "native/launcher/app/renderer.js").read_text(encoding="utf-8")
    assert "lastPayloadFingerprint" in js
    assert "setText(" in js
    assert "statusText').innerHTML" not in js
    assert "renderCommandLists(); setupTabs(); bindBaseButtons(); bindImport();" in js
    assert js.count("addEventListener('click'") < 20


def test_runtime_shell_has_stable_control_bar_and_status_spans():
    html = (ROOT / "native/launcher/app/index.html").read_text(encoding="utf-8")
    css = (ROOT / "native/launcher/app/styles.css").read_text(encoding="utf-8")
    assert 'id="staticControlBar"' in html
    assert 'id="statusWord"' in html
    assert 'id="statusDots"' in html
    assert 'id="statusStar"' in html
    assert "static controls never reflow" in css
    assert ".button-row { display: grid" in css


def test_tauri_and_launcher_share_runtime_page_logic():
    launcher_js = (ROOT / "native/launcher/app/renderer.js").read_text(encoding="utf-8")
    tauri_js = (ROOT / "native/tauri/src/main.js").read_text(encoding="utf-8")
    assert launcher_js == tauri_js
