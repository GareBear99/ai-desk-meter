from ai_meter.protocol import BackendState, UsagePayload


def test_payload_serializes_backend_state():
    payload = UsagePayload(
        service="arc-rar",
        current_percent=10,
        weekly_percent=5,
        current_reset_seconds=1,
        weekly_reset_seconds=2,
        backend=BackendState(name="Arc-RAR", receipt_state="available"),
    )
    wire = payload.to_wire()
    assert wire["schema"] == "ai-desk-meter.v1"
    assert wire["backend"]["name"] == "Arc-RAR"
    assert wire["backend"]["receipt_state"] == "available"


def test_payload_limits_warning_count_and_length():
    payload = UsagePayload(
        current_percent=0,
        weekly_percent=0,
        current_reset_seconds=0,
        weekly_reset_seconds=0,
        warnings=["x" * 500 for _ in range(20)],
    )
    wire = payload.to_wire()
    assert len(wire["warnings"]) == 10
    assert len(wire["warnings"][0]) == 160
