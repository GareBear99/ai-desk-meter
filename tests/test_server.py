from __future__ import annotations

import json
import threading
from contextlib import closing
from http.client import HTTPConnection
from socket import socket

from ai_meter.server import MeterRequestHandler, ThreadingHTTPServer


def _free_port() -> int:
    with closing(socket()) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _start_server():
    port = _free_port()
    server = ThreadingHTTPServer(("127.0.0.1", port), MeterRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


def _get(port: int, path: str):
    conn = HTTPConnection("127.0.0.1", port, timeout=3)
    conn.request("GET", path)
    response = conn.getresponse()
    body = response.read().decode("utf-8")
    conn.close()
    return response.status, json.loads(body or "{}")


def test_health_endpoint():
    server, port = _start_server()
    try:
        status, data = _get(port, "/health")
        assert status == 200
        assert data["ok"] is True
        assert data["service"] == "ai-desk-meter"
    finally:
        server.shutdown()
        server.server_close()


def test_providers_endpoint_lists_mock():
    server, port = _start_server()
    try:
        status, data = _get(port, "/providers")
        assert status == 200
        assert "mock" in data["providers"]
        assert "arcrar-cli" in data["providers"]
    finally:
        server.shutdown()
        server.server_close()


def test_status_endpoint_returns_payload():
    server, port = _start_server()
    try:
        status, data = _get(port, "/status?provider=mock")
        assert status == 200
        assert data["schema"] == "ai-desk-meter.v1"
        assert data["source"] == "mock"
    finally:
        server.shutdown()
        server.server_close()


def test_diagnostics_endpoint_excludes_private_content():
    server, port = _start_server()
    try:
        status, data = _get(port, "/diagnostics?provider=mock")
        assert status == 200
        assert data["schema"] == "ai-desk-meter.diagnostics.v1"
        assert "private prompts" in data["note"]
    finally:
        server.shutdown()
        server.server_close()
