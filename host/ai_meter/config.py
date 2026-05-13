from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class AppConfig:
    provider: str = "mock"
    transport: str = "stdout"
    poll_seconds: int = 30
    url: str = "http://127.0.0.1/api/state"


def load_config(path: str | None = None) -> AppConfig:
    if not path:
        return AppConfig()
    p = Path(path).expanduser()
    if not p.exists():
        return AppConfig()
    data = json.loads(p.read_text(encoding="utf-8"))
    device = data.get("device", {})
    provider = data.get("provider", {})
    return AppConfig(
        provider=provider.get("active", "mock"),
        transport=device.get("transport", "stdout"),
        poll_seconds=int(provider.get("poll_seconds", 30)),
        url=device.get("wifi_url", "http://127.0.0.1/api/state"),
    )
