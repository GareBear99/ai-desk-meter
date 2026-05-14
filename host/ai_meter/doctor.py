from __future__ import annotations

from time import time
from typing import Any

from ai_meter import __version__
from ai_meter.companion import to_companion_payload
from ai_meter.diagnostics import safe_environment
from ai_meter.providers import make_provider, provider_names


def run_doctor(provider: str = "mock") -> dict[str, Any]:
    """Run a small local health report without requiring Arc-RAR or hardware.

    The doctor command is intentionally conservative: it proves the Python host,
    provider registry, payload validation, companion conversion, and safe
    environment reporting work. Backend-specific failures are returned as
    warnings/errors inside the provider payload instead of raising.
    """

    checks: list[dict[str, Any]] = []

    names = provider_names()
    checks.append({"name": "provider_registry", "ok": bool(names), "providers": names})

    try:
        payload = make_provider(provider).read()
        wire = payload.to_wire()
        checks.append({"name": "provider_payload", "ok": wire.get("schema") == "ai-desk-meter.v1", "source": wire.get("source")})
    except Exception as exc:  # defensive CLI boundary
        wire = {}
        checks.append({"name": "provider_payload", "ok": False, "error": str(exc)[:160]})

    try:
        companion = to_companion_payload(make_provider(provider).read())
        checks.append({"name": "companion_payload", "ok": companion.get("schema") == "ai_desk_meter_companion_v1"})
    except Exception as exc:
        checks.append({"name": "companion_payload", "ok": False, "error": str(exc)[:160]})

    ok = all(bool(item.get("ok")) for item in checks)
    return {
        "schema": "ai-desk-meter.doctor.v1",
        "ok": ok,
        "app": {"name": "ai-desk-meter", "version": __version__},
        "provider": provider,
        "generated_at": int(time()),
        "checks": checks,
        "environment": safe_environment(),
        "note": "Doctor output excludes tokens, prompts, API keys, and private AI session content.",
    }
