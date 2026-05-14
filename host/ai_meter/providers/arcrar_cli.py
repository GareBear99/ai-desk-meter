from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any, Sequence

from pydantic import ValidationError

from ai_meter.protocol import BackendState, BurnRate, Confidence, MeterMode, UsagePayload


ENV_ARCRAR_BIN = "AI_METER_ARCRAR_BIN"
ENV_ARCRAR_TIMEOUT = "AI_METER_ARCRAR_TIMEOUT"
DEFAULT_ARCRAR_BIN = "arc-rar"
DEFAULT_TIMEOUT_SECONDS = 3.0


@dataclass(frozen=True)
class ArcRarCommandSpec:
    """A single Arc-RAR CLI command consumed by AI Desk Meter."""

    name: str
    argv: tuple[str, ...]
    required: bool = False


COMMAND_SPECS: tuple[ArcRarCommandSpec, ...] = (
    ArcRarCommandSpec("status", ("status", "--json"), required=True),
    ArcRarCommandSpec("receipt_latest", ("receipts", "latest", "--json")),
    ArcRarCommandSpec("archive_verify", ("archive", "verify", "--json")),
    ArcRarCommandSpec("session_inspect", ("session", "inspect", "--json")),
)


class ArcRarCliProvider:
    """Arc-RAR CLI provider with fail-closed subprocess handling.

    The provider consumes Arc-RAR through a command boundary instead of importing
    Arc-RAR internals. The required command is ``arc-rar status --json``. Receipt,
    archive, and session commands are optional enrichment commands; if an
    enrichment command fails the dashboard still receives the required status
    payload with a warning instead of crashing.
    """

    name = "arcrar-cli"

    def __init__(self, executable: str | None = None, timeout_seconds: float | None = None, enrich: bool = True):
        self.enrich = enrich
        self.executable = executable or os.environ.get(ENV_ARCRAR_BIN, DEFAULT_ARCRAR_BIN)
        if timeout_seconds is None:
            timeout_seconds = float(os.environ.get(ENV_ARCRAR_TIMEOUT, DEFAULT_TIMEOUT_SECONDS))
        self.timeout_seconds = max(0.25, float(timeout_seconds))

    def read(self) -> UsagePayload:
        resolved = shutil.which(self.executable)
        if resolved is None:
            return self._offline(f"Arc-RAR executable not found: {self.executable}")

        command_results: dict[str, dict[str, Any] | None] = {}
        warnings: list[str] = []

        for spec in (COMMAND_SPECS if self.enrich else COMMAND_SPECS[:1]):
            try:
                command_results[spec.name] = self._run_json_command([resolved, *spec.argv])
            except subprocess.TimeoutExpired:
                message = f"Arc-RAR command timed out: {' '.join(spec.argv)} after {self.timeout_seconds:g}s"
                if spec.required:
                    return self._error(message)
                warnings.append(message)
                command_results[spec.name] = None
            except subprocess.CalledProcessError as exc:
                detail = _safe_stderr(exc.stderr) or f"exit code {exc.returncode}"
                message = f"Arc-RAR command failed: {' '.join(spec.argv)} ({detail})"
                if spec.required:
                    return self._error(message)
                warnings.append(message)
                command_results[spec.name] = None
            except json.JSONDecodeError as exc:
                message = f"Arc-RAR command did not return valid JSON: {' '.join(spec.argv)} ({exc.msg})"
                if spec.required:
                    return self._error(message)
                warnings.append(message)
                command_results[spec.name] = None
            except OSError as exc:
                message = f"Arc-RAR command could not be executed: {' '.join(spec.argv)} ({exc})"
                if spec.required:
                    return self._offline(message)
                warnings.append(message)
                command_results[spec.name] = None

        try:
            return self._payload_from_cli_bundle(command_results, extra_warnings=warnings)
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
        parsed = json.loads(completed.stdout)
        if not isinstance(parsed, dict):
            raise ValueError("Arc-RAR JSON output must be an object")
        return parsed

    def _payload_from_cli_bundle(
        self,
        command_results: dict[str, dict[str, Any] | None],
        extra_warnings: list[str] | None = None,
    ) -> UsagePayload:
        status_raw = command_results.get("status") or {}
        receipt_raw = command_results.get("receipt_latest") or {}
        archive_raw = command_results.get("archive_verify") or {}
        session_raw = command_results.get("session_inspect") or {}

        return self._payload_from_cli(
            status_raw,
            receipt_raw=receipt_raw,
            archive_raw=archive_raw,
            session_raw=session_raw,
            extra_warnings=extra_warnings or [],
        )

    def _payload_from_cli(
        self,
        raw: dict[str, Any],
        *,
        receipt_raw: dict[str, Any] | None = None,
        archive_raw: dict[str, Any] | None = None,
        session_raw: dict[str, Any] | None = None,
        extra_warnings: list[str] | None = None,
    ) -> UsagePayload:
        # Accept either a full AI Desk Meter payload shape or a compact Arc-RAR
        # backend status shape. This keeps the adapter useful during backend
        # contract stabilization without weakening validation.
        receipt_raw = receipt_raw or {}
        archive_raw = archive_raw or {}
        session_raw = session_raw or {}
        backend_raw = raw.get("backend") or raw.get("arc") or raw
        usage_raw = raw.get("usage") or raw

        receipt_state = _first_text(
            backend_raw.get("receipt_state"),
            backend_raw.get("receipts"),
            receipt_raw.get("receipt_state"),
            receipt_raw.get("state"),
            "available" if _first_text(receipt_raw.get("id"), receipt_raw.get("receipt_id")) else None,
            default="unknown",
        )
        archive_state = _first_text(
            backend_raw.get("archive_state"),
            backend_raw.get("archive"),
            archive_raw.get("archive_state"),
            archive_raw.get("state"),
            "verified" if archive_raw.get("verified") is True else None,
            "failed" if archive_raw.get("verified") is False else None,
            default="unknown",
        )
        hardwire_state = _first_text(
            backend_raw.get("hardwire_state"),
            backend_raw.get("hardwire"),
            session_raw.get("hardwire_state"),
            "portable" if session_raw.get("portable") is True else None,
            "not_portable" if session_raw.get("portable") is False else None,
            default="unknown",
        )
        checkpoint_id = _first_text(
            backend_raw.get("checkpoint_id"),
            backend_raw.get("last_checkpoint"),
            receipt_raw.get("checkpoint_id"),
            receipt_raw.get("id"),
            receipt_raw.get("receipt_id"),
            session_raw.get("checkpoint_id"),
            default=None,
        )

        backend = BackendState(
            name=_first_text(backend_raw.get("name"), backend_raw.get("backend"), default="Arc-RAR"),
            receipt_state=receipt_state,
            archive_state=archive_state,
            hardwire_state=hardwire_state,
            checkpoint_id=checkpoint_id,
        )

        mode_value = str(raw.get("mode", "active"))
        status_value = str(raw.get("status", "Arc-RAR CLI linked"))
        confidence_value = str(raw.get("confidence", "estimated"))

        warnings = _clean_messages(raw.get("warnings", [])) + _clean_messages(extra_warnings or [])
        errors = _clean_messages(raw.get("errors", []))
        if archive_state in {"failed", "corrupt", "invalid"}:
            errors.append(f"Arc-RAR archive verify reported {archive_state}")

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
            warnings=warnings,
            errors=errors,
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


def _first_text(*values: Any, default: str | None = "unknown") -> str | None:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return default


def _clean_messages(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    cleaned: list[str] = []
    for item in values:
        text = str(item).strip()
        if text:
            cleaned.append(text[:160])
    return cleaned[:10]


def _safe_stderr(stderr: str | bytes | None) -> str:
    if stderr is None:
        return ""
    if isinstance(stderr, bytes):
        stderr = stderr.decode("utf-8", errors="replace")
    return " ".join(stderr.strip().split())[:160]
