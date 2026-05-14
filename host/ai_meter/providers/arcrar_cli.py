from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any, Sequence

from pydantic import ValidationError

from ai_meter.protocol import BackendState, BurnRate, Confidence, MeterMode, UsagePayload


ENV_ARCRAR_BIN = "AI_METER_ARCRAR_BIN"
ENV_ARCRAR_TIMEOUT = "AI_METER_ARCRAR_TIMEOUT"
DEFAULT_ARCRAR_BIN = "arc-rar"
DEFAULT_TIMEOUT_SECONDS = 3.0


class ArcRarCliProvider:
    """Arc-RAR CLI provider with fail-closed subprocess handling.

    This provider consumes a stable Arc-RAR command boundary instead of importing
    Arc-RAR internals. Missing executables, timeouts, non-zero exits, invalid JSON,
    and schema mismatches are converted into dashboard-safe payloads.
    """

    name = "arcrar-cli"

    def __init__(self, executable: str | None = None, timeout_seconds: float | None = None):
        self.executable = executable or os.environ.get(ENV_ARCRAR_BIN, DEFAULT_ARCRAR_BIN)
        if timeout_seconds is None:
            timeout_seconds = float(os.environ.get(ENV_ARCRAR_TIMEOUT, DEFAULT_TIMEOUT_SECONDS))
        self.timeout_seconds = max(0.25, float(timeout_seconds))

    def read(self) -> UsagePayload:
        resolved = shutil.which(self.executable)
        if resolved is None:
            return self._offline(f"Arc-RAR executable not found: {self.executable}")

        try:
            raw = self._run_json_command([resolved, "status", "--json"])
        except subprocess.TimeoutExpired:
            return self._error(f"Arc-RAR command timed out after {self.timeout_seconds:g}s")
        except subprocess.CalledProcessError as exc:
            detail = _safe_stderr(exc.stderr) or f"exit code {exc.returncode}"
            return self._error(f"Arc-RAR command failed: {detail}")
        except json.JSONDecodeError as exc:
            return self._error(f"Arc-RAR command did not return valid JSON: {exc.msg}")
        except OSError as exc:
            return self._offline(f"Arc-RAR command could not be executed: {exc}")

        try:
            return self._payload_from_cli(raw)
        except (TypeError, ValueError, ValidationError) as exc:
            return self._error(f"Arc-RAR CLI output failed validation: {exc}")

    def _run_json_command(self, command: Sequence[str]) -> dict[str, Any]:
        completed = subprocess.run(
            list(command),
            check=True,
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
        )
        return json.loads(completed.stdout)

    def _payload_from_cli(self, raw: dict[str, Any]) -> UsagePayload:
        # Accept either a full AI Desk Meter payload shape or a compact Arc-RAR
        # backend status shape. This keeps the adapter useful during backend
        # contract stabilization without weakening validation.
        backend_raw = raw.get("backend") or raw.get("arc") or raw
        usage_raw = raw.get("usage") or raw

        backend = BackendState(
            name=str(backend_raw.get("name", "Arc-RAR")),
            receipt_state=str(backend_raw.get("receipt_state", backend_raw.get("receipts", "unknown"))),
            archive_state=str(backend_raw.get("archive_state", backend_raw.get("archive", "unknown"))),
            hardwire_state=str(backend_raw.get("hardwire_state", backend_raw.get("hardwire", "unknown"))),
            checkpoint_id=backend_raw.get("checkpoint_id") or backend_raw.get("last_checkpoint"),
        )

        mode_value = str(raw.get("mode", "active"))
        status_value = str(raw.get("status", "Arc-RAR CLI linked"))
        confidence_value = str(raw.get("confidence", "estimated"))

        return UsagePayload(
            service=str(raw.get("service", "arc-rar")),
            current_percent=float(usage_raw.get("current_percent", usage_raw.get("current", 0))),
            weekly_percent=float(usage_raw.get("weekly_percent", usage_raw.get("weekly", 0))),
            current_reset_seconds=int(usage_raw.get("current_reset_seconds", usage_raw.get("current_reset", 0))),
            weekly_reset_seconds=int(usage_raw.get("weekly_reset_seconds", usage_raw.get("weekly_reset", 0))),
            burn_rate=BurnRate(str(raw.get("burn_rate", usage_raw.get("burn_rate", "idle")))),
            status=status_value,
            mode=MeterMode(mode_value),
            source=self.name,
            confidence=Confidence(confidence_value),
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
            status="Arc-RAR CLI offline",
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
            status="Arc-RAR CLI error",
            mode=MeterMode.error,
            source=self.name,
            confidence=Confidence.unknown,
            backend=BackendState(name="Arc-RAR"),
            errors=[error],
        )


def _safe_stderr(stderr: str | bytes | None) -> str:
    if stderr is None:
        return ""
    if isinstance(stderr, bytes):
        stderr = stderr.decode("utf-8", errors="replace")
    return " ".join(stderr.strip().split())[:160]
