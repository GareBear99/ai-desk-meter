from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_linux_sbc_scripts_exist_and_are_executable():
    install = ROOT / "scripts" / "install_linux_sbc.sh"
    smoke = ROOT / "scripts" / "run_smoke_test.sh"
    assert install.exists()
    assert smoke.exists()
    assert install.stat().st_mode & 0o111
    assert smoke.stat().st_mode & 0o111


def test_systemd_and_env_artifacts_exist():
    assert (ROOT / "deploy" / "systemd" / "ai-desk-meter.service").exists()
    assert (ROOT / "examples" / "systemd.env.example").exists()


def test_character_and_license_docs_preserve_product_direction():
    character = (ROOT / "docs" / "character-spec.md").read_text(encoding="utf-8")
    license_doc = (ROOT / "docs" / "licensing-roadmap.md").read_text(encoding="utf-8")
    assert "Musing..." in character
    assert "MuseMeter 3.0" in license_doc
    assert "Open source" in license_doc


def test_public_dashboard_preserves_pixel_buddy_and_musing_state():
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "pixel-buddy" in html
    assert "✶ Musing..." in html
    assert "MuseMeter 3.0" in html


def test_companion_firmware_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "firmware" / "esp32_companion_display" / "ai_desk_meter_companion.ino").exists()
    assert (root / "firmware" / "arduino_serial_companion" / "ai_desk_meter_serial.ino").exists()
    assert (root / "docs" / "hardware-companion-protocol.md").exists()
