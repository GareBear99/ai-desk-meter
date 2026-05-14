from __future__ import annotations

import json
import time
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


def read_provider_payload(provider_name: str) -> UsagePayload:
    return make_provider(provider_name).read()


def write_status(path: Path, provider_name: str) -> Path:
    payload = read_provider_payload(provider_name)
    return atomic_write_json(path, payload.to_wire())


def write_companion(path: Path, provider_name: str) -> Path:
    payload = read_provider_payload(provider_name)
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
    interval_seconds = max(0.25, float(interval_seconds))
    written = 0
    while True:
        out = write_companion(path, provider_name) if companion else write_status(path, provider_name)
        written += 1
        if on_write:
            on_write(out)
        if count is not None and written >= count:
            return written
        time.sleep(interval_seconds)
