from __future__ import annotations

import json
import os
from pathlib import Path
from time import time
from typing import Any

from ai_meter.protocol import BackendState, BurnRate, Confidence, MeterMode, UsagePayload


class OmnibinaryProvider:
    """Fails-closed adapter stub for the future Omnibinary event-spine backend.

    This provider intentionally does not pretend Omnibinary is already wired. By
    default it returns an offline/planned payload. During contract testing or
    early integration work, AI_METER_OMNIBINARY_STATE can point at a local JSON
    fixture matching docs/omnibinary-adapter-spec.md.
    """

    name = "omnibinary"

    def __init__(self, state_path: str | None = None) -> None:
        self.state_path = state_path or os.getenv("AI_METER_OMNIBINARY_STATE")

    def read(self) -> UsagePayload:
        if not self.state_path:
            return self._planned_payload("Omnibinary adapter planned")

        path = Path(self.state_path)
        if not path.exists():
            return self._planned_payload(f"Omnibinary state file not found: {path}")

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return self._error_payload(f"invalid Omnibinary state JSON: {exc}")

        return self._from_state(raw)

    def _from_state(self, raw: dict[str, Any]) -> UsagePayload:
        event = raw.get("event", {}) if isinstance(raw.get("event"), dict) else {}
        replay = raw.get("replay", {}) if isinstance(raw.get("replay"), dict) else {}
        health = raw.get("health", {}) if isinstance(raw.get("health"), dict) else {}

        linked = bool(raw.get("linked", False))
        warning_items = _clean_list(raw.get("warnings", []))
        error_items = _clean_list(raw.get("errors", []))
        event_state = str(event.get("state", "unknown"))
        replay_state = str(replay.get("state", "unknown"))
        hardwire_state = str(health.get("hardwire_state", "unknown"))
        checkpoint_id = raw.get("checkpoint_id") or event.get("checkpoint_id")

        mode = MeterMode.active if linked and not error_items else MeterMode.error if error_items else MeterMode.offline
        status = raw.get("status") or ("Omnibinary linked" if linked else "Omnibinary offline")
        confidence = Confidence.estimated if linked else Confidence.unknown

        current_percent = _percent(raw.get("current_percent", raw.get("usage", {}).get("current", 0)))
        weekly_percent = _percent(raw.get("weekly_percent", raw.get("usage", {}).get("weekly", 0)))

        return UsagePayload(
            service="omnibinary",
            current_percent=current_percent,
            weekly_percent=weekly_percent,
            current_reset_seconds=_nonnegative_int(raw.get("current_reset_seconds", 0)),
            weekly_reset_seconds=_nonnegative_int(raw.get("weekly_reset_seconds", 0)),
            burn_rate=_burn_rate(raw.get("burn_rate", "idle")),
            status=str(status)[:64],
            mode=mode,
            updated_at=_nonnegative_int(raw.get("updated_at", int(time()))),
            source=self.name,
            confidence=confidence,
            backend=BackendState(
                name="Omnibinary",
                receipt_state=event_state,
                archive_state=replay_state,
                hardwire_state=hardwire_state,
                checkpoint_id=str(checkpoint_id) if checkpoint_id else None,
            ),
            warnings=warning_items,
            errors=error_items,
        )

    def _planned_payload(self, reason: str) -> UsagePayload:
        return UsagePayload(
            service="omnibinary",
            current_percent=0,
            weekly_percent=0,
            current_reset_seconds=0,
            weekly_reset_seconds=0,
            burn_rate=BurnRate.idle,
            status="Omnibinary planned",
            mode=MeterMode.offline,
            updated_at=int(time()),
            source=self.name,
            confidence=Confidence.unknown,
            backend=BackendState(
                name="Omnibinary",
                receipt_state="planned",
                archive_state="planned",
                hardwire_state="planned",
            ),
            warnings=[reason],
            errors=[],
        )

    def _error_payload(self, reason: str) -> UsagePayload:
        return UsagePayload(
            service="omnibinary",
            current_percent=0,
            weekly_percent=0,
            current_reset_seconds=0,
            weekly_reset_seconds=0,
            burn_rate=BurnRate.idle,
            status="Omnibinary error",
            mode=MeterMode.error,
            updated_at=int(time()),
            source=self.name,
            confidence=Confidence.unknown,
            backend=BackendState(name="Omnibinary"),
            warnings=[],
            errors=[reason],
        )


def _clean_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip()[:160] for item in value if str(item).strip()][:10]


def _percent(value: Any) -> float:
    try:
        return round(max(0.0, min(100.0, float(value))), 1)
    except Exception:
        return 0.0


def _nonnegative_int(value: Any) -> int:
    try:
        return max(0, int(value))
    except Exception:
        return 0


def _burn_rate(value: Any) -> BurnRate:
    try:
        return BurnRate(str(value))
    except Exception:
        return BurnRate.idle
