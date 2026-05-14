from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import time
from typing import Any
from urllib.parse import parse_qs, urlparse

from ai_meter import __version__
from ai_meter.companion import to_companion_payload
from ai_meter.diagnostics import build_diagnostics_payload
from ai_meter.providers import make_provider, provider_names


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8787


def _json_bytes(data: dict[str, Any], status: int = 200) -> tuple[int, bytes]:
    return status, json.dumps(data, indent=2, sort_keys=True).encode("utf-8")


class MeterRequestHandler(BaseHTTPRequestHandler):
    server_version = "AIDeskMeterHTTP/0.6"

    def do_OPTIONS(self) -> None:  # noqa: N802 - stdlib hook name
        self._send_json({}, 204)

    def do_GET(self) -> None:  # noqa: N802 - stdlib hook name
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        provider = query.get("provider", ["mock"])[0]

        if parsed.path == "/health":
            self._send_json(
                {
                    "ok": True,
                    "service": "ai-desk-meter",
                    "version": __version__,
                    "time": int(time()),
                }
            )
            return

        if parsed.path == "/providers":
            self._send_json({"providers": provider_names(), "default": "mock"})
            return

        if parsed.path == "/status":
            self._send_json(self._read_provider(provider))
            return

        if parsed.path == "/companion/status":
            self._send_json(self._read_companion(provider))
            return

        if parsed.path == "/diagnostics":
            self._send_json(build_diagnostics_payload(provider))
            return

        self._send_json({"error": "not_found", "path": parsed.path}, 404)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - stdlib signature
        # Keep CLI output quiet by default. Errors are returned as JSON payloads.
        return

    def _read_provider(self, provider: str) -> dict[str, Any]:
        try:
            payload = make_provider(provider).read()
            return payload.to_wire()
        except Exception as exc:  # defensive API boundary
            return {
                "schema": "ai-desk-meter.v1",
                "service": provider,
                "current_percent": 0,
                "weekly_percent": 0,
                "current_reset_seconds": 0,
                "weekly_reset_seconds": 0,
                "burn_rate": "idle",
                "status": "Provider error",
                "mode": "error",
                "updated_at": int(time()),
                "source": provider,
                "confidence": "unknown",
                "backend": {"name": provider},
                "warnings": [],
                "errors": [f"provider failed: {exc}"[:160]],
            }

    def _read_companion(self, provider: str) -> dict[str, Any]:
        try:
            payload = make_provider(provider).read()
            return to_companion_payload(payload)
        except Exception as exc:  # defensive API boundary
            return {
                "schema": "ai_desk_meter_companion_v1",
                "status": "error",
                "current_pct": 0,
                "weekly_pct": 0,
                "current_reset": "0m",
                "weekly_reset": "0m",
                "activity": "error",
                "message": "Provider error",
                "burn_rate": "idle",
                "backend": provider,
                "receipt_state": "unknown",
                "archive_state": "unknown",
                "hardwire_state": "unknown",
                "warnings": 0,
                "errors": 1,
                "updated_at": int(time()),
                "error": f"provider failed: {exc}"[:160],
            }

    def _send_json(self, data: dict[str, Any], status: int = 200) -> None:
        status_code, body = _json_bytes(data, status)
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if status_code != 204:
            self.wfile.write(body)


def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    httpd = ThreadingHTTPServer((host, port), MeterRequestHandler)
    print(f"AI Desk Meter API listening on http://{host}:{port}")
    print("Endpoints: /health /providers /status?provider=mock /companion/status?provider=mock /diagnostics?provider=mock")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
