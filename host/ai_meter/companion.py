from __future__ import annotations

from typing import Any

from ai_meter.protocol import MeterMode, UsagePayload

COMPANION_SCHEMA = "ai_desk_meter_companion_v1"


def clamp_int_percent(value: float) -> int:
    return int(round(max(0, min(100, float(value)))))


def format_duration(seconds: int) -> str:
    seconds = max(0, int(seconds))
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def infer_activity(payload: UsagePayload) -> str:
    if payload.errors:
        return "error"
    if payload.mode == MeterMode.offline:
        return "offline"
    if payload.mode == MeterMode.stale:
        return "stale"
    if payload.warnings:
        return "warning"
    # The baseline character/state intentionally uses Musing while an agent is
    # responding to prompt input or an action is loading. Later product versions
    # can split this into responding/loading/action states without breaking v1.
    return "musing"


def to_companion_payload(payload: UsagePayload) -> dict[str, Any]:
    backend = payload.backend
    return {
        "schema": COMPANION_SCHEMA,
        "status": "linked" if payload.mode == MeterMode.active and not payload.errors else str(payload.mode.value),
        "current_pct": clamp_int_percent(payload.current_percent),
        "weekly_pct": clamp_int_percent(payload.weekly_percent),
        "current_reset": format_duration(payload.current_reset_seconds),
        "weekly_reset": format_duration(payload.weekly_reset_seconds),
        "activity": infer_activity(payload),
        "message": payload.status[:48],
        "burn_rate": str(payload.burn_rate.value),
        "backend": payload.source,
        "receipt_state": backend.receipt_state if backend else "unknown",
        "archive_state": backend.archive_state if backend else "unknown",
        "hardwire_state": backend.hardwire_state if backend else "unknown",
        "warnings": len(payload.warnings),
        "errors": len(payload.errors),
        "updated_at": payload.updated_at,
    }
