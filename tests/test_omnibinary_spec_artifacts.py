import json
from pathlib import Path

from ai_meter.providers import provider_names
from ai_meter.providers.omnibinary import OmnibinaryProvider

ROOT = Path(__file__).resolve().parents[1]


def test_omnibinary_docs_and_fixtures_exist():
    required = [
        "docs/omnibinary-adapter-spec.md",
        "docs/arc-core-hardwire-map.md",
        "docs/adapter-boundaries.md",
        "examples/omnibinary_event_state.example.json",
        "examples/omnibinary_replay_state.example.json",
        "examples/omnibinary_error_state.example.json",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_omnibinary_provider_is_registered():
    assert "omnibinary" in provider_names()


def test_omnibinary_provider_fails_closed_without_state():
    payload = OmnibinaryProvider().read().to_wire()
    assert payload["source"] == "omnibinary"
    assert payload["mode"] == "offline"
    assert payload["backend"]["receipt_state"] == "planned"
    assert payload["warnings"]
    assert payload["errors"] == []


def test_omnibinary_provider_maps_valid_fixture():
    fixture = ROOT / "examples/omnibinary_event_state.example.json"
    payload = OmnibinaryProvider(state_path=str(fixture)).read().to_wire()
    assert payload["mode"] == "active"
    assert payload["current_percent"] == 12
    assert payload["weekly_percent"] == 3
    assert payload["backend"]["name"] == "Omnibinary"
    assert payload["backend"]["receipt_state"] == "available"
    assert payload["backend"]["archive_state"] == "ready"
    assert payload["backend"]["hardwire_state"] == "portable"
    assert payload["backend"]["checkpoint_id"] == "ob_chk_001"


def test_omnibinary_provider_preserves_error_fixture():
    fixture = ROOT / "examples/omnibinary_error_state.example.json"
    payload = OmnibinaryProvider(state_path=str(fixture)).read().to_wire()
    assert payload["mode"] == "error"
    assert payload["errors"] == ["Omnibinary event source unavailable."]


def test_omnibinary_examples_are_valid_json():
    for rel in [
        "examples/omnibinary_event_state.example.json",
        "examples/omnibinary_replay_state.example.json",
        "examples/omnibinary_error_state.example.json",
    ]:
        data = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        assert data["schema"] == "omnibinary.adapter_state.v1"
