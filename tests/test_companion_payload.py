from __future__ import annotations

from ai_meter.companion import format_duration, to_companion_payload
from ai_meter.protocol import BackendState, BurnRate, Confidence, MeterMode, UsagePayload


def test_format_duration_compact():
    assert format_duration(0) == "0m"
    assert format_duration(82 * 60) == "1h 22m"
    assert format_duration(6 * 86400 + 8 * 3600) == "6d 8h"


def test_companion_payload_from_usage_payload():
    payload = UsagePayload(
        service="arc-rar",
        current_percent=49.6,
        weekly_percent=10.6,
        current_reset_seconds=82 * 60,
        weekly_reset_seconds=6 * 86400 + 8 * 3600,
        burn_rate=BurnRate.normal,
        status="✶ Musing...",
        mode=MeterMode.active,
        source="arcrar-cli",
        confidence=Confidence.estimated,
        backend=BackendState(name="Arc-RAR", receipt_state="available", archive_state="verified", hardwire_state="portable"),
        muse_connected=True,
        muse_state="musing",
    )
    compact = to_companion_payload(payload)
    assert compact["schema"] == "ai_desk_meter_companion_v1"
    assert compact["status"] == "linked"
    assert compact["current_pct"] == 50
    assert compact["weekly_pct"] == 11
    assert compact["current_reset"] == "1h 22m"
    assert compact["weekly_reset"] == "6d 8h"
    assert compact["activity"] == "musing"
    assert compact["receipt_state"] == "available"


def test_companion_payload_errors_drive_activity_error():
    payload = UsagePayload(
        service="bad",
        status="Provider error",
        mode=MeterMode.error,
        source="mock",
        errors=["bad"],
    )
    compact = to_companion_payload(payload)
    assert compact["status"] == "error"
    assert compact["activity"] == "error"
    assert compact["errors"] == 1
