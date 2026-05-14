from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_native_gui_docs_exist():
    required = [
        "docs/native-gui-plan.md",
        "docs/tauri-shell-plan.md",
        "docs/desktop-security.md",
        "native/tauri/README.md",
        "native/tauri/tauri.conf.example.json",
        "native/tauri/src-tauri-notes.md",
        "native/tauri/frontend-bridge.md",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_native_launch_scripts_exist_and_preserve_loopback_default():
    sh = ROOT / "scripts/launch_local_dashboard.sh"
    ps1 = ROOT / "scripts/launch_local_dashboard.ps1"
    assert sh.exists()
    assert ps1.exists()
    assert "127.0.0.1" in sh.read_text(encoding="utf-8")
    assert "127.0.0.1" in ps1.read_text(encoding="utf-8")


def test_tauri_config_is_example_not_bundle_claim():
    config = (ROOT / "native/tauri/tauri.conf.example.json").read_text(encoding="utf-8")
    assert "AI Desk Meter" in config
    assert '"active": false' in config.lower()
    assert "127.0.0.1:8787" in config
