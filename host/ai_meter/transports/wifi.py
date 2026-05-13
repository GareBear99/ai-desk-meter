from __future__ import annotations

import requests

from ai_meter.protocol import UsagePayload


class WifiTransport:
    name = "wifi"

    def __init__(self, url: str, timeout: float = 5.0):
        self.url = url
        self.timeout = timeout

    def send(self, payload: UsagePayload) -> None:
        response = requests.post(self.url, json=payload.to_wire(), timeout=self.timeout)
        response.raise_for_status()
