from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Any

from ai_meter.companion import to_companion_payload
from ai_meter.protocol import UsagePayload
from ai_meter.providers import make_provider


def atomic_write_json(path: Path, data: dict[str, Any]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    return path


def _stamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def enrich_payload(payload: UsagePayload, *, provider_name: str, action: str, checker_state: str = "active") -> UsagePayload:
    stamp = _stamp()
    existing_log = list(payload.run_log or [])
    generated = [
        f"[{stamp}] CLI checker: {checker_state}",
        f"[{stamp}] provider {provider_name} sampled",
        f"[{stamp}] last action: {action}",
        f"[{stamp}] action in progress: {payload.action_in_progress or 'musing'}",
    ]
    payload.last_action = action
    payload.runtime_connected = getattr(payload, "runtime_connected", True)
    payload.muse_connected = bool(getattr(payload, "muse_connected", False))
    payload.muse_state = getattr(payload, "muse_state", "musing" if payload.muse_connected else "none") or ("musing" if payload.muse_connected else "none")
    payload.action_in_progress = payload.action_in_progress or ("musing" if payload.muse_connected else "none")
    payload.cli_checker = {
        "state": checker_state,
        "last_check": int(time.time()),
        "message": f"{action} via ai-meter",
    }
    payload.run_log = (existing_log + generated)[-12:]
    return payload


def read_provider_payload(provider_name: str, action: str = "provider payload refreshed") -> UsagePayload:
    payload = make_provider(provider_name).read()
    return enrich_payload(payload, provider_name=provider_name, action=action)


def write_status(path: Path, provider_name: str) -> Path:
    payload = read_provider_payload(provider_name, action="write-status complete")
    return atomic_write_json(path, payload.to_wire())


def write_companion(path: Path, provider_name: str) -> Path:
    payload = read_provider_payload(provider_name, action="write-companion complete")
    return atomic_write_json(path, to_companion_payload(payload))


def watch_writer(
    *,
    path: Path,
    provider_name: str,
    interval_seconds: float,
    companion: bool = False,
    count: int | None = None,
    on_write: Callable[[Path], None] | None = None,
) -> int:
    interval_seconds = max(0.1, float(interval_seconds))
    written = 0
    while True:
        out = write_companion(path, provider_name) if companion else write_status(path, provider_name)
        written += 1
        if on_write:
            on_write(out)
        if count is not None and written >= count:
            return written
        time.sleep(interval_seconds)
