from __future__ import annotations

import json
import os
import platform
import sys
import zipfile
from pathlib import Path
from time import time
from typing import Any

from ai_meter import __version__
from ai_meter.providers import make_provider, provider_names


def build_diagnostics_payload(provider: str = "mock") -> dict[str, Any]:
    errors: list[str] = []
    payload: dict[str, Any]
    try:
        payload = make_provider(provider).read().to_wire()
    except Exception as exc:
        payload = {}
        errors.append(f"provider failed: {exc}"[:160])

    return {
        "schema": "ai-desk-meter.diagnostics.v1",
        "generated_at": int(time()),
        "app": {"name": "ai-desk-meter", "version": __version__},
        "provider": provider,
        "available_providers": provider_names(),
        "payload": payload,
        "environment": safe_environment(),
        "errors": errors,
        "note": "Diagnostics intentionally exclude tokens, API keys, private prompts, and private AI session content.",
    }


def safe_environment() -> dict[str, Any]:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "system": platform.system(),
        "release": platform.release(),
        "cwd": str(Path.cwd()),
        "env_flags": {
            "AI_METER_ARCRAR_STATE": bool(os.environ.get("AI_METER_ARCRAR_STATE")),
            "AI_METER_ARCRAR_BIN": bool(os.environ.get("AI_METER_ARCRAR_BIN")),
            "AI_METER_ARCRAR_TIMEOUT": bool(os.environ.get("AI_METER_ARCRAR_TIMEOUT")),
        },
    }


def write_diagnostics_zip(out_path: str | Path, provider: str = "mock") -> Path:
    out = Path(out_path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    data = build_diagnostics_payload(provider)

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("payload.json", json.dumps(data.get("payload", {}), indent=2, sort_keys=True))
        zf.writestr("diagnostics.json", json.dumps(data, indent=2, sort_keys=True))
        zf.writestr("provider.txt", f"provider={provider}\navailable={','.join(provider_names())}\n")
        zf.writestr("environment.txt", json.dumps(data["environment"], indent=2, sort_keys=True))
        zf.writestr("errors.json", json.dumps(data.get("errors", []), indent=2))
        zf.writestr(
            "README_DIAGNOSTICS.txt",
            "AI Desk Meter diagnostics bundle. This bundle is designed to exclude secrets, tokens, private prompts, and private AI session content.\n",
        )
    return out
