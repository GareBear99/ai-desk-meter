from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ai_meter.protocol import BackendState, BurnRate, Confidence, MeterMode, UsagePayload


DEFAULT_STATE_PATH = "./arcrar_meter_state.json"
ENV_STATE_PATH = "AI_METER_ARCRAR_STATE"


class ArcRarProvider:
    """Conservative Arc-RAR state-file provider.

    This provider intentionally reads a stable JSON state file instead of importing
    Arc-RAR internals. That keeps AI Desk Meter portable while the backend command
    contract matures.
    """

    name = "arcrar"

    def __init__(self, state_path: str | None = None):
        self.state_path = Path(state_path or os.environ.get(ENV_STATE_PATH, DEFAULT_STATE_PATH)).expanduser()

    def read(self) -> UsagePayload:
        if not self.state_path.exists():
            return self._offline(f"Arc-RAR state file not found: {self.state_path}")

        try:
            raw = json.loads(self.state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return self._error(f"Arc-RAR state file is not valid JSON: {exc.msg}")
        except OSError as exc:
            return self._error(f"Arc-RAR state file could not be read: {exc}")

        try:
            return self._payload_from_state(raw)
        except (TypeError, ValueError, ValidationError) as exc:
            return self._error(f"Arc-RAR state file failed validation: {exc}")

    def _payload_from_state(self, raw: dict[str, Any]) -> UsagePayload:
        backend_raw = raw.get("backend") or {}
        backend = BackendState(
            name=str(backend_raw.get("name", "Arc-RAR")),
            receipt_state=str(backend_raw.get("receipt_state", "unknown")),
            archive_state=str(backend_raw.get("archive_state", "unknown")),
            hardwire_state=str(backend_raw.get("hardwire_state", "unknown")),
            checkpoint_id=backend_raw.get("checkpoint_id"),
        )

        return UsagePayload(
            service=str(raw.get("service", "arc-rar")),
            current_percent=float(raw.get("current_percent", 0)),
            weekly_percent=float(raw.get("weekly_percent", 0)),
            current_reset_seconds=int(raw.get("current_reset_seconds", 0)),
            weekly_reset_seconds=int(raw.get("weekly_reset_seconds", 0)),
            burn_rate=BurnRate(str(raw.get("burn_rate", "idle"))),
            status=str(raw.get("status", "Arc-RAR linked")),
            mode=MeterMode(str(raw.get("mode", "active"))),
            source=self.name,
            confidence=Confidence(str(raw.get("confidence", "estimated"))),
            backend=backend,
            warnings=list(raw.get("warnings", [])),
            errors=list(raw.get("errors", [])),
        )

    def _offline(self, warning: str) -> UsagePayload:
        return UsagePayload(
            service="arc-rar",
            current_percent=0,
            weekly_percent=0,
            current_reset_seconds=0,
            weekly_reset_seconds=0,
            burn_rate=BurnRate.idle,
            status="Arc-RAR offline",
            mode=MeterMode.offline,
            source=self.name,
            confidence=Confidence.unknown,
            backend=BackendState(name="Arc-RAR"),
            warnings=[warning],
        )

    def _error(self, error: str) -> UsagePayload:
        return UsagePayload(
            service="arc-rar",
            current_percent=0,
            weekly_percent=0,
            current_reset_seconds=0,
            weekly_reset_seconds=0,
            burn_rate=BurnRate.idle,
            status="Arc-RAR error",
            mode=MeterMode.error,
            source=self.name,
            confidence=Confidence.unknown,
            backend=BackendState(name="Arc-RAR"),
            errors=[error],
        )
