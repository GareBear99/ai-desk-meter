import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_native_gui_docs_exist():
    required = [
        "docs/native-gui-plan.md",
        "docs/tauri-shell-plan.md",
        "docs/desktop-security.md",
        "docs/release-v1.0.2.md",
        "native/tauri/README.md",
        "native/tauri/frontend-bridge.md",
        "native/catalina/README.md",
        "native/catalina/ai_desk_meter_catalina.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_real_tauri_app_files_exist():
    required = [
        "native/tauri/package.json",
        "native/tauri/index.html",
        "native/tauri/src/main.js",
        "native/tauri/src/styles.css",
        "native/tauri/public/pixel-buddy-musing.svg",
        "native/tauri/public/sample-status.json",
        "native/tauri/src-tauri/icons/icon.png",
        "native/tauri/src-tauri/Cargo.toml",
        "native/tauri/src-tauri/tauri.conf.json",
        "native/tauri/src-tauri/build.rs",
        "native/tauri/src-tauri/src/main.rs",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_tauri_package_scripts_are_present():
    package = json.loads((ROOT / "native/tauri/package.json").read_text(encoding="utf-8"))
    scripts = package["scripts"]
    assert scripts["dev"] == "vite --host 127.0.0.1 --port 1420"
    assert scripts["tauri:dev"] == "tauri dev"
    assert scripts["tauri:build"] == "tauri build"
    assert "@tauri-apps/api" in package["dependencies"]
    assert "@tauri-apps/cli" in package["devDependencies"]


def test_tauri_config_is_real_bundle_config():
    config = json.loads((ROOT / "native/tauri/src-tauri/tauri.conf.json").read_text(encoding="utf-8"))
    assert config["productName"] == "AI Desk Meter"
    assert config["version"] == "1.2.1"
    assert config["bundle"]["active"] is True
    assert config["build"]["frontendDist"] == "../dist"


def test_native_app_preserves_no_server_payload_flow_and_character():
    main_rs = (ROOT / "native/tauri/src-tauri/src/main.rs").read_text(encoding="utf-8")
    main_js = (ROOT / "native/tauri/src/main.js").read_text(encoding="utf-8")
    index = (ROOT / "native/tauri/index.html").read_text(encoding="utf-8")
    assert "read_status_file" in main_rs
    assert "runtime/status.json" in main_rs
    assert "AI_METER_STATUS_PATH" in main_rs
    assert "read_status_file" in main_js
    assert "getTauriInvoke" in main_js
    assert "payloadFile" in main_js
    assert "✶ Musing..." in main_js
    assert "No active Muse" in main_js
    assert "browser preview awaiting runtime/status.json" in main_js
    assert "sample-status.json" not in main_js
    assert "setConnectionState" in main_js
    assert "isRuntimePayload" in main_js
    assert "isMusePayload" in main_js
    assert "Runtime connected" in main_js
    assert "last_action" in main_js
    assert "run_log" in main_js
    assert "muse-eye" in index
    assert "buddy-eye" not in index


def test_native_launch_scripts_exist_and_preserve_loopback_default():
    sh = ROOT / "scripts/launch_local_dashboard.sh"
    ps1 = ROOT / "scripts/launch_local_dashboard.ps1"
    assert sh.exists()
    assert ps1.exists()
    assert "127.0.0.1" in sh.read_text(encoding="utf-8")
    assert "127.0.0.1" in ps1.read_text(encoding="utf-8")


def test_legacy_tauri_example_config_removed():
    assert not (ROOT / "native/tauri/tauri.conf.example.json").exists()


def test_native_frontend_has_musing_animation_and_action_panels():
    index = (ROOT / "native/tauri/index.html").read_text(encoding="utf-8")
    css = (ROOT / "native/tauri/src/styles.css").read_text(encoding="utf-8")
    assert "muse-eye" in index
    assert "blink-eye" not in index
    assert "dots" in (ROOT / "native/tauri/src/main.js").read_text(encoding="utf-8")
    assert "lastAction" in index
    assert "actionProgress" in index
    assert "cliChecker" in index
    assert "runLogOutput" in index
    assert "No active Muse" in index
    assert "blink-eyes" in css
    assert "buddy-eye" not in css
    assert "eyes-closed" not in css
    assert "@keyframes blink" not in css
    assert "@keyframes dotPulse" in css


def test_catalina_fallback_is_no_server_and_reads_status_json():
    script = (ROOT / "native/catalina/ai_desk_meter_catalina.py").read_text(encoding="utf-8")
    assert "runtime/status.json" in script
    assert "tkinter" in script
    assert "Musing" in script
    assert "No active Muse" in script
    assert "run_log" in script
    assert "cli_checker" in script


def test_runtime_page_exposes_diy_cost_specs():
    text = (ROOT / "native" / "launcher" / "app" / "index.html").read_text(encoding="utf-8")
    assert "DIY / Cost Specs" in text
    assert "$50–$120" in text
    assert "Waveshare ESP32-S3-Touch-AMOLED-2.16" in text
    assert "Parts & Sourcing" in text
    assert "Waveshare official store" in text
    assert "Amazon / regional marketplace" in text

def test_docs_page_links_diy_cost_specs():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "DIY / Cost Specs" in text
    assert "Back to Runtime Dashboard" in text


def test_parts_and_sourcing_doc_is_build_ready():
    text = (ROOT / "docs" / "parts-and-sourcing.md").read_text(encoding="utf-8")
    assert "Waveshare ESP32-S3-Touch-AMOLED-2.16" in text
    assert "ESP32-S3-Touch-AMOLED-2.16" in text
    assert "USB-C" in text
    assert "Raspberry Pi" in text
    assert "Amazon / regional marketplace" in text
    assert "Espressif Component Registry" in text
    assert "$50–$120" in text
